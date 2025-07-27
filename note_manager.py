"""
note_manager.py
~~~~~~~~~~~~~~~~

This script implements a simple note‑taking system using Python’s
standard library. Notes are stored in a SQLite database, which means
you don’t need any external dependencies. The command‑line interface
supports creating notes, listing all notes, searching notes by keyword
and exporting notes to JSON or CSV formats. A very basic license key
check is included; in practice you would want a more secure licensing
system.

Example usage::

    # Create a new note
    python note_manager.py --email user@example.com --license abc --command add \
        --title "My first note" --body "This is a note body."

    # List all notes
    python note_manager.py --email user@example.com --license abc --command list

    # Search notes containing a keyword
    python note_manager.py --email user@example.com --license abc --command search \
        --query "first"

    # Export notes to JSON
    python note_manager.py --email user@example.com --license abc --command export \
        --format json --output notes.json

When run for the first time, the script will create a SQLite database file
named ``notes.db`` in the current working directory. Subsequent runs
will reuse this database. Each note has a title, body and timestamp.

Disclaimer: the licensing mechanism provided here is intentionally
simplistic and should not be used in production. For real products,
consider integrating a dedicated licensing or payment solution and
consult legal counsel if necessary. This script is provided under the
MIT license without warranty.
"""

import argparse
import csv
import json
import os
import sqlite3
from datetime import datetime
from hashlib import md5
from typing import Iterable, Optional


DB_NAME = "notes.db"


def verify_license(email: str, key: str) -> bool:
    """Check that the license key matches the email.

    For demonstration purposes this simply checks whether the first three
    characters of the MD5 hex digest of the email equal the supplied
    key (case‑insensitive). In a production setting you would want a
    more secure scheme.
    """
    digest = md5(email.encode("utf-8")).hexdigest()
    return digest.startswith(key.lower())


class NoteManager:
    """A simple SQLite-backed note manager."""

    def __init__(self, db_path: str = DB_NAME) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create the notes table if it doesn’t exist."""
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_note(self, title: str, body: str) -> None:
        """Insert a new note into the database."""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO notes (title, body, created_at) VALUES (?, ?, ?)",
            (title, body, datetime.utcnow().isoformat()),
        )
        self.conn.commit()

    def list_notes(self) -> Iterable[tuple[int, str, str, str]]:
        """Return all notes from the database."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, body, created_at FROM notes ORDER BY id ASC")
        return cur.fetchall()

    def search_notes(self, query: str) -> Iterable[tuple[int, str, str, str]]:
        """Return notes containing the query in title or body (case-insensitive)."""
        cur = self.conn.cursor()
        like = f"%{query.lower()}%"
        cur.execute(
            """
            SELECT id, title, body, created_at
            FROM notes
            WHERE LOWER(title) LIKE ? OR LOWER(body) LIKE ?
            ORDER BY id ASC
            """,
            (like, like),
        )
        return cur.fetchall()

    def export_notes(self, fmt: str, output_path: str, notes: Optional[Iterable] = None) -> None:
        """Export notes to JSON or CSV.

        Args:
            fmt: 'json' or 'csv'.
            output_path: Path to write the export file.
            notes: Iterable of notes to export. If None, export all notes.
        """
        data = list(notes if notes is not None else self.list_notes())
        if fmt.lower() == "json":
            export_data = [
                {"id": n[0], "title": n[1], "body": n[2], "created_at": n[3]}
                for n in data
            ]
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2)
        elif fmt.lower() == "csv":
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "title", "body", "created_at"])
                writer.writerows(data)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'csv'.")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Manage personal notes stored in SQLite.")
    parser.add_argument("--email", required=True, help="Registration email address")
    parser.add_argument("--license", dest="license_key", required=True, help="License key")
    parser.add_argument(
        "--command",
        choices=["add", "list", "search", "export"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument("--title", help="Title of the note (required for add)")
    parser.add_argument("--body", help="Body of the note (required for add)")
    parser.add_argument("--query", help="Keyword to search notes")
    parser.add_argument("--format", choices=["json", "csv"], help="Export format")
    parser.add_argument("--output", help="Path to export file")
    args = parser.parse_args(argv)

    # License verification
    if not verify_license(args.email, args.license_key):
        parser.error("Invalid license. Please supply a valid key.")

    nm = NoteManager()
    cmd = args.command
    if cmd == "add":
        if not args.title or not args.body:
            parser.error("--title and --body are required for the add command")
        nm.add_note(args.title, args.body)
        print(f"Note added with title: {args.title}")
    elif cmd == "list":
        rows = nm.list_notes()
        if rows:
            for row in rows:
                print(f"[{row[0]}] {row[1]} (created {row[3]}):\n{row[2]}\n")
        else:
            print("No notes found.")
    elif cmd == "search":
        if not args.query:
            parser.error("--query is required for the search command")
        matches = nm.search_notes(args.query)
        if matches:
            for row in matches:
                print(f"[{row[0]}] {row[1]} (created {row[3]}):\n{row[2]}\n")
        else:
            print(f"No notes matching '{args.query}' were found.")
    elif cmd == "export":
        if not args.format or not args.output:
            parser.error("--format and --output are required for export")
        nm.export_notes(args.format, args.output)
        print(f"Notes exported to {args.output} in {args.format} format.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
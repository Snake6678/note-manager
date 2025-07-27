"""
note_manager.py — Simple command-line note manager with license check

Features:
- Add notes with a title and body
- List all notes
- Search notes by keyword
- Export notes to JSON or CSV
- Basic license key validation (MD5-based, 3-letter prefix)

Author: You
License: MIT
"""

import argparse
import sqlite3
import json
import csv
from datetime import datetime
from hashlib import md5

DB_NAME = "notes.db"


def verify_license(email: str, key: str) -> bool:
    digest = md5(email.encode("utf-8")).hexdigest()
    return digest.startswith(key.lower())


class NoteManager:
    def __init__(self, db_path=DB_NAME):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_note(self, title: str, body: str):
        timestamp = datetime.utcnow().isoformat()
        self.conn.execute(
            "INSERT INTO notes (title, body, created_at) VALUES (?, ?, ?)",
            (title, body, timestamp)
        )
        self.conn.commit()
        print(f"Note added with title: {title}")

    def list_notes(self):
        cursor = self.conn.execute("SELECT title, body, created_at FROM notes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        for title, body, created_at in rows:
            print(f"- {title}\n  {body}\n  [{created_at}]\n")

    def search_notes(self, keyword: str):
        cursor = self.conn.execute(
            "SELECT title, body, created_at FROM notes WHERE title LIKE ? OR body LIKE ?",
            (f"%{keyword}%", f"%{keyword}%")
        )
        rows = cursor.fetchall()
        if not rows:
            print("No matching notes found.")
        for title, body, created_at in rows:
            print(f"- {title}\n  {body}\n  [{created_at}]\n")

    def export_notes(self, format: str, output: str):
        cursor = self.conn.execute("SELECT title, body, created_at FROM notes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        if format == "json":
            with open(output, "w") as f:
                json.dump([{"title": t, "body": b, "created_at": c} for t, b, c in rows], f, indent=2)
            print(f"Notes exported to {output} in JSON format.")
        elif format == "csv":
            with open(output, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["title", "body", "created_at"])
                writer.writerows(rows)
            print(f"Notes exported to {output} in CSV format.")
        else:
            print("Unsupported format. Use 'json' or 'csv'.")


def main():
    parser = argparse.ArgumentParser(description="Command-line note manager")
    parser.add_argument("--email", required=True)
    parser.add_argument("--license", required=True)
    parser.add_argument("--command", choices=["add", "list", "search", "export"], required=True)
    parser.add_argument("--title")
    parser.add_argument("--body")
    parser.add_argument("--query")
    parser.add_argument("--format", choices=["json", "csv"])
    parser.add_argument("--output")

    args = parser.parse_args()

    if not verify_license(args.email, args.license):
        print("Invalid license. Please supply a valid key.")
        return

    manager = NoteManager()

    if args.command == "add":
        if not args.title or not args.body:
            print("Title and body are required for adding a note.")
            return
        manager.add_note(args.title, args.body)

    elif args.command == "list":
        manager.list_notes()

    elif args.command == "search":
        if not args.query:
            print("Query is required for searching.")
            return
        manager.search_notes(args.query)

    elif args.command == "export":
        if not args.format or not args.output:
            print("Both format and output file name are required for export.")
            return
        manager.export_notes(args.format, args.output)


if __name__ == "__main__":
    main()

diff --git a/note_manager.py b/note_manager.py
index d96722edf452bffa02c4373537a1b26c4ffe66d9..085ab78d3f22a378dc8010b4c90fb550efd2c872 100644
--- a/note_manager.py
+++ b/note_manager.py
@@ -1,85 +1,51 @@
-"""
-note_manager.py
-~~~~~~~~~~~~~~~~
-
-This script implements a simple note‑taking system using Python’s
-standard library. Notes are stored in a SQLite database, which means
-you don’t need any external dependencies. The command‑line interface
-supports creating notes, listing all notes, searching notes by keyword
-and exporting notes to JSON or CSV formats. A very basic license key
-check is included; in practice you would want a more secure licensing
-system.
-
-Example usage::
-
-    # Create a new note
-    python note_manager.py --email user@example.com --license abc --command add \
-        --title "My first note" --body "This is a note body."
-
-    # List all notes
-    python note_manager.py --email user@example.com --license abc --command list
-
-    # Search notes containing a keyword
-    python note_manager.py --email user@example.com --license abc --command search \
-        --query "first"
-
-    # Export notes to JSON
-    python note_manager.py --email user@example.com --license abc --command export \
-        --format json --output notes.json
-
-When run for the first time, the script will create a SQLite database file
-named ``notes.db`` in the current working directory. Subsequent runs
-will reuse this database. Each note has a title, body and timestamp.
-
-Disclaimer: the licensing mechanism provided here is intentionally
-simplistic and should not be used in production. For real products,
-consider integrating a dedicated licensing or payment solution and
-consult legal counsel if necessary. This script is provided under the
-MIT license without warranty.
+"""Small command-line note manager.
+
+Notes are stored in a local SQLite database. The utility lets you add,
+list, search and export notes. A trivial license check demonstrates how
+one might tie a license key to an email address by comparing a prefix of
+its MD5 hash.
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
-    """Check that the license key matches the email.
+    """Return ``True`` if the license key appears valid for ``email``.
 
-    For demonstration purposes this simply checks whether the first three
-    characters of the MD5 hex digest of the email equal the supplied
-    key (case‑insensitive). In a production setting you would want a
-    more secure scheme.
+    The demo implementation compares the first three characters of the
+    email's MD5 hex digest to ``key`` (case-insensitive).
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



if __name__ == "__main__":
    raise SystemExit(main())

# Note Manager

A simple Python note-taking app with both a command-line interface and a desktop GUI (built with `tkinter`). Notes are stored in a local SQLite database, and you can add, list, delete, and export them.

---

##  Features

- Add notes (title + body)
- List all saved notes
-️ Delete notes by title
- Export notes to `JSON` or `CSV`
-️ Clean, minimal GUI
- Lightweight & offline — no cloud, no logins

---

## 💻 Run the GUI

```bash
python3 gui.py
```

---

##  Use From the Command Line

```bash
# Add a new note
python3 note_manager.py --email your@email.com --license 56f --command add --title "My Note" --body "This is the body."

# List all notes
python3 note_manager.py --email your@email.com --license 56f --command list

# Delete a note by title
python3 note_manager.py --email your@email.com --license 56f --command delete --title "My Note"

# Export notes to JSON
python3 note_manager.py --email your@email.com --license 56f --command export --format json --output notes.json

# Export notes to CSV
python3 note_manager.py --email your@email.com --license 56f --command export --format csv --output notes.csv
```

---

##  License Key

To generate your license key, run:

```bash
python3 -c "import hashlib; print(hashlib.md5('your@email.com'.encode()).hexdigest()[:3])"
```

Replace `'your@email.com'` with your real email.

---

##  Requirements

- Python 3.x  
- No external libraries needed (`tkinter`, `sqlite3`, `argparse`, etc. are built-in)

---

##  Screenshots

_Add screenshots of the GUI and terminal here (optional but recommended)_


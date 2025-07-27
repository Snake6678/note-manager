# Note Manager

Note Manager is a lightweight Python application that allows you to create, edit, delete, and export notes. It offers both a command-line interface and a graphical user interface (GUI) built with `tkinter`. Notes are stored locally using SQLite.

This version includes voice-to-text note entry and basic math expression evaluation using SymPy.

## Features

- Add notes with title and body
- Edit existing notes by selecting them from the list
- Scrollable list of saved notes
- Delete notes by title
- Export notes to JSON or CSV format
- Desktop GUI built with tkinter
- Voice recognition for note input (speech-to-text)
- Evaluate math expressions written in notes (e.g., `sqrt(16) + 3^2`)
- Works offline with no login or cloud required

## How to Run the App (GUI)

```bash
python3 gui.py


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


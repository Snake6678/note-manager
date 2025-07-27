import tkinter as tk
from tkinter import messagebox, simpledialog
from note_manager import NoteManager

root = tk.Tk()
root.title("Note Manager")

manager = NoteManager()

# Title input
tk.Label(root, text="Title").pack(pady=(10, 0))
title_entry = tk.Entry(root, width=40)
title_entry.pack(pady=5)

# Body input
tk.Label(root, text="Body").pack()
body_entry = tk.Text(root, height=5, width=40)
body_entry.pack(pady=5)

# Add note
def add_note():
    title = title_entry.get()
    body = body_entry.get("1.0", tk.END).strip()
    if not title or not body:
        messagebox.showwarning("Input Error", "Both title and body are required.")
        return
    manager.add_note(title, body)
    messagebox.showinfo("Success", "Note added successfully!")
    title_entry.delete(0, tk.END)
    body_entry.delete("1.0", tk.END)

# List notes
def list_notes():
    notes = manager.list_notes()
    if not notes:
        messagebox.showinfo("Notes", "No notes found.")
        return
    notes_text = ""
    for note in notes:
        notes_text += f"{note[1]} - {note[2]}\n[{note[3]}]\n\n"
    messagebox.showinfo("All Notes", notes_text)

# Export notes
def export_notes():
    file_format = simpledialog.askstring("Export Format", "Enter format: json or csv")
    if file_format not in ["json", "csv"]:
        messagebox.showerror("Error", "Invalid format.")
        return
    output_file = f"exported_notes.{file_format}"
    try:
        manager.export_notes(file_format, output_file)
        messagebox.showinfo("Success", f"Notes exported to {output_file}")
    except Exception as e:
        messagebox.showerror("Export Failed", str(e))

def delete_note():
    title = simpledialog.askstring("Delete Note", "Enter title of note to delete:")
    if not title:
        return
    manager.delete_note_by_title(title)
    messagebox.showinfo("Deleted", f"Note with title '{title}' deleted (if it existed).")

# Buttons
tk.Button(root, text="Add Note", width=20, command=add_note).pack(pady=5)
tk.Button(root, text="List Notes", width=20, command=list_notes).pack(pady=5)
tk.Button(root, text="Export Notes", width=20, command=export_notes).pack(pady=5)
tk.Button(root, text="Delete Note", width=20, command=delete_note).pack(pady=5)

root.mainloop()


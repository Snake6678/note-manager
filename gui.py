import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import speech_recognition as sr
from note_manager import NoteManager
from sympy import symbols, Eq, solve
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

def evaluate_math():
    expr_text = body_entry.get("1.0", tk.END).strip()
    transformations = standard_transformations + (implicit_multiplication_application,)

    try:
        # Extract variable names like 'x', 'y'
        variables = set(filter(str.isalpha, expr_text.replace("=", "").replace(" ", "")))
        symbols_dict = {v: symbols(v) for v in variables}

        if "=" in expr_text:
            left, right = expr_text.split("=")
            left_expr = parse_expr(left, transformations=transformations, local_dict=symbols_dict)
            right_expr = parse_expr(right, transformations=transformations, local_dict=symbols_dict)
            equation = Eq(left_expr, right_expr)
            result = solve(equation)
            messagebox.showinfo("Solution", f"Solution: {result}")
        else:
            expr = parse_expr(expr_text, transformations=transformations, local_dict=symbols_dict)
            result = expr.evalf()
            messagebox.showinfo("Result", f"{expr_text} = {result}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not parse the math expression.\n\n{e}")

# Init GUI
root = tk.Tk()
root.title("Note Manager")

manager = NoteManager()

# Input fields
tk.Label(root, text="Title").pack()
title_entry = tk.Entry(root, width=40)
title_entry.pack()

tk.Label(root, text="Body").pack()
body_entry = tk.Text(root, height=5, width=40)
body_entry.pack()

# Status label
status_label = tk.Label(root, text="", fg="black")
status_label.pack()

# Scrollable note list
tk.Label(root, text="Your Notes").pack()
frame = tk.Frame(root)
frame.pack()

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

note_listbox = tk.Listbox(frame, width=40, height=8, yscrollcommand=scrollbar.set)
note_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=note_listbox.yview)

# Recognizer
recording = False
recognizer = sr.Recognizer()
audio_data = None

def toggle_recording():
    global recording, audio_data
    if not recording:
        recording = True
        status_label.config(text="🎙️ Recording... Press again to stop.")
        threading.Thread(target=start_listening).start()
    else:
        recording = False
        status_label.config(text="🔄 Processing...")
        try:
            text = recognizer.recognize_google(audio_data)
            body_entry.insert(tk.END, text)
            status_label.config(text="✅ Voice note added.")
        except sr.UnknownValueError:
            status_label.config(text="❌ Could not understand.")
        except sr.RequestError:
            status_label.config(text="🚫 API error.")

def start_listening():
    global audio_data
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        status_label.config(text="🎤 Listening now...")
        audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=None)

def add_note():
    title = title_entry.get().strip()
    body = body_entry.get("1.0", tk.END).strip()
    if not title or not body:
        messagebox.showwarning("Error", "Title and body are required.")
        return
    manager.update_note_by_title(title, title, body)  # Overwrites existing
    refresh_note_list()
    messagebox.showinfo("Saved", "Note saved successfully.")
    title_entry.delete(0, tk.END)
    body_entry.delete("1.0", tk.END)

def delete_note():
    title = simpledialog.askstring("Delete Note", "Enter title to delete:")
    if not title:
        return
    manager.delete_note_by_title(title)
    refresh_note_list()
    messagebox.showinfo("Deleted", f"Deleted note titled: {title}")

def export_notes():
    manager.export_notes("json", "notes.json")
    manager.export_notes("csv", "notes.csv")
    messagebox.showinfo("Exported", "Notes saved to notes.json and notes.csv.")

def refresh_note_list():
    note_listbox.delete(0, tk.END)
    for title, _, _ in manager.list_notes():
        note_listbox.insert(tk.END, title)

def on_note_select(event):
    if not note_listbox.curselection():
        return
    index = note_listbox.curselection()[0]
    title, body, _ = manager.list_notes()[index]
    title_entry.delete(0, tk.END)
    title_entry.insert(0, title)
    body_entry.delete("1.0", tk.END)
    body_entry.insert(tk.END, body)

def evaluate_math():
    expression = body_entry.get("1.0", tk.END).strip()
    if not expression:
        messagebox.showwarning("Input Error", "Please enter a math expression in the Body field.")
        return
    try:
        result = sympify(expression).evalf()
        messagebox.showinfo("Result", f"Result: {result}")
    except SympifyError:
        messagebox.showerror("Invalid Expression", "Could not parse the math expression.")

note_listbox.bind("<<ListboxSelect>>", on_note_select)

# Buttons
tk.Button(root, text="Add Note", width=20, command=add_note).pack(pady=3)
tk.Button(root, text="🎙️ Record Note", width=20, command=toggle_recording).pack(pady=3)
tk.Button(root, text="Export Notes", width=20, command=export_notes).pack(pady=3)
tk.Button(root, text="Delete Note", width=20, command=delete_note).pack(pady=3)
tk.Button(root, text="🧮 Solve Math", width=20, command=evaluate_math).pack(pady=3)

refresh_note_list()
root.mainloop()


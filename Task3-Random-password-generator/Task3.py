import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    length = length_entry.get()

    if not length.isdigit() or int(length) < 4:
        messagebox.showerror("Invalid Input", "Please enter a valid number (minimum 4)")
        return

    length = int(length)

    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()
    avoid_similar = similar_var.get()

    if not (use_upper or use_lower or use_digits or use_symbols):
        messagebox.showerror("Error", "Please select at least one character type!")
        return

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()_+=-{}[];:/?.<>"

    # Remove similar looking characters
    similar_chars = "Il1O0"

    if avoid_similar:
        upper = ''.join(c for c in upper if c not in similar_chars)
        lower = ''.join(c for c in lower if c not in similar_chars)
        digits = ''.join(c for c in digits if c not in similar_chars)
        symbols = ''.join(c for c in symbols if c not in similar_chars)

    char_pool = ""
    if use_upper: char_pool += upper
    if use_lower: char_pool += lower
    if use_digits: char_pool += digits
    if use_symbols: char_pool += symbols

    password = ''.join(random.choice(char_pool) for _ in range(length))
    result_entry.delete(0, tk.END)
    result_entry.insert(0, password)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(result_entry.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# GUI
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x400")

tk.Label(root, text="Password Length:", font=("Arial", 12)).pack()
length_entry = tk.Entry(root, font=("Arial", 12))
length_entry.pack()

upper_var = tk.IntVar()
lower_var = tk.IntVar()
digits_var = tk.IntVar()
symbols_var = tk.IntVar()
similar_var = tk.IntVar()

tk.Checkbutton(root, text="Include Uppercase (A-Z)", variable=upper_var).pack()
tk.Checkbutton(root, text="Include Lowercase (a-z)", variable=lower_var).pack()
tk.Checkbutton(root, text="Include Digits (0-9)", variable=digits_var).pack()
tk.Checkbutton(root, text="Include Symbols (!@#$...)", variable=symbols_var).pack()
tk.Checkbutton(root, text="Avoid Similar Characters (1 l I 0 O)", variable=similar_var).pack()

tk.Button(root, text="Generate Password", command=generate_password, bg="lightgreen").pack(pady=10)

result_entry = tk.Entry(root, font=("Arial", 14), width=25)
result_entry.pack(pady=10)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="lightblue").pack()

root.mainloop()

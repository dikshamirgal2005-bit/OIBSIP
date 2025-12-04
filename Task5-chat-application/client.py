import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog
from tkinter import messagebox
import base64
import os

HOST = '127.0.0.1'
PORT = 5000

# ---------------- Networking ---------------- #
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except:
    messagebox.showerror("Connection Error", "Cannot connect to server.")
    exit()

username = input("Enter username: ")
client.send(username.encode())

# ---------------- GUI ---------------- #
root = tk.Tk()
root.title(f"Chat App - {username}")
root.geometry("550x580")

chat_area = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

message_entry = tk.Entry(root, font=("Arial", 14))
message_entry.pack(padx=10, pady=5, fill=tk.X)


# ---------------- Emoji Picker ---------------- #
emojis = ["😀", "😂", "😍", "😎", "😡", "😢", "👍", "🙏", "🔥", "❤️"]

def open_emoji_window():
    win = tk.Toplevel(root)
    win.title("Emoji Picker")
    win.geometry("300x200")

    for e in emojis:
        btn = tk.Button(win, text=e, font=("Arial", 20),
                        command=lambda emoji=e: insert_emoji(emoji))
        btn.pack(side=tk.LEFT, padx=5, pady=5)

def insert_emoji(emoji):
    message_entry.insert(tk.END, emoji)


emoji_btn = tk.Button(root, text="😊 Emoji", command=open_emoji_window)
emoji_btn.pack(pady=5)


# ---------------- Send Message ---------------- #
def send_message():
    msg = message_entry.get().strip()
    if msg:
        try:
            client.send(f"TEXT::{username}: {msg}".encode())
            message_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Message not sent. Server might be down.")

send_btn = tk.Button(root, text="Send", command=send_message)
send_btn.pack(pady=5)


# ---------------- File Sending ---------------- #
def send_file():
    documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
    filepath = filedialog.askopenfilename(initialdir=documents_folder)

    if not filepath:
        return
    
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    filename = os.path.basename(filepath)
    message = f"FILE::{username}::{filename}::{data}"

    try:
        client.send(message.encode())
    except:
        messagebox.showerror("Error", "Could not send file.")

file_btn = tk.Button(root, text="📁 Send File", command=send_file)
file_btn.pack(pady=5)


# ---------------- Receive Messages ---------------- #
def receive_messages():
    while True:
        try:
            message = client.recv(500000).decode()

            if message.startswith("FILE::"):
                _, sender, fname, filedata = message.split("::", 3)

                save_path = os.path.join(os.path.expanduser("~"),
                                         "Documents",
                                         f"received_{fname}")

                with open(save_path, "wb") as f:
                    f.write(base64.b64decode(filedata))

                text = f"{sender} sent a file: {fname}\nSaved in Documents.\n\n"

                chat_area.config(state='normal')
                chat_area.insert(tk.END, text)
                chat_area.yview(tk.END)
                chat_area.config(state='disabled')

            else:
                chat_area.config(state='normal')
                chat_area.insert(tk.END, message + "\n")
                chat_area.yview(tk.END)
                chat_area.config(state='disabled')

        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()

root.bind('<Return>', lambda event: send_message())
root.mainloop()
client.close()

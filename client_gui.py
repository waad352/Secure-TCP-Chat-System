import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- الاتصال بالسيرفر ---
def connect_to_server():
    username = username_entry.get().strip()
    if not username:
        messagebox.showwarning("Error", "Please enter a username!")
        return

    try:
        global client_socket, current_username
        current_username = username
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 5555))
        client_socket.send(username.encode("utf-8"))

        login_window.destroy()
        open_chat_window(username)

    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

# --- نافذة المحادثة ---
def open_chat_window(username):
    global chat_window, message_input, chat_area

    chat_window = tk.Tk()
    chat_window.title(f"Chat - {username}")
    chat_window.geometry("550x450")
    chat_window.configure(bg="#f4f4f4")

    chat_area = scrolledtext.ScrolledText(
        chat_window, 
        state='disabled', 
        wrap=tk.WORD, 
        font=("Arial", 11), 
        bg="white", 
        relief="sunken"
    )
    chat_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    bottom_frame = tk.Frame(chat_window, bg="#f4f4f4")
    bottom_frame.pack(fill=tk.X, pady=10)

    message_input = tk.Entry(bottom_frame, font=("Arial", 12), width=50, relief="groove", justify="center")
    message_input.pack(side=tk.LEFT, expand=True, padx=(40, 10))
    message_input.bind("<Return>", lambda event: send_message())

    send_button = tk.Button(
        bottom_frame,
        text="Send",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 11, "bold"),
        width=10,
        command=send_message
    )
    send_button.pack(side=tk.RIGHT, padx=(0, 40))

    threading.Thread(target=receive_messages, daemon=True).start()

    chat_window.protocol(
        "WM_DELETE_WINDOW",
        lambda: (client_socket.close() if client_socket else None, chat_window.destroy())
    )
    chat_window.mainloop()

# --- إرسال الرسائل ---
def send_message():
    message = message_input.get().strip()
    if message:
        try:
            # إرسال الرسالة إلى السيرفر
            client_socket.send(message.encode("utf-8"))
            # عرض الرسالة محليًا أيضًا باسم المستخدم
            chat_area.config(state='normal')
            chat_area.insert(tk.END, f"You: {message}\n")
            chat_area.config(state='disabled')
            chat_area.yview(tk.END)
            message_input.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Message not sent: {e}")

# --- استقبال الرسائل ---
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            chat_area.config(state='normal')
            chat_area.insert(tk.END, message + "\n")
            chat_area.config(state='disabled')
            chat_area.yview(tk.END)
        except:
            break

# --- نافذة تسجيل الدخول ---
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x150")
login_window.configure(bg="#f4f4f4")

tk.Label(login_window, text="Enter Username:", bg="#f4f4f4", font=("Arial", 11)).pack(pady=10)
username_entry = tk.Entry(login_window, width=30, bg="white", relief="sunken")
username_entry.pack(pady=5, padx=20, fill=tk.X)

tk.Button(login_window, text="Connect", command=connect_to_server, bg="#2196F3", fg="white", width=10).pack(pady=10)

login_window.mainloop()

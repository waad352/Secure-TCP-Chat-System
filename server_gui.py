import socket
import threading

# تخزين العملاء وأسمائهم
clients = []
usernames = []

def broadcast(message, client_socket=None):
    """إرسال الرسالة لجميع العملاء باستثناء المرسل"""
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                # إذا حدث خطأ أثناء الإرسال نحذف العميل
                clients.remove(client)

def handle_client(client_socket):
    """التعامل مع كل مستخدم متصل"""
    index = clients.index(client_socket)
    username = usernames[index]

    while True:
        try:
            # استقبال الرسالة من المستخدم
            message = client_socket.recv(1024)
            if not message:
                break

            # ✅ طباعة في السيرفر عندما يرسل المستخدم رسالة
            print(f"[SERVER LOG] {username} sent a message: {message.decode('utf-8')}")

            # بث الرسالة لبقية المستخدمين
            broadcast(f"{username}: {message.decode('utf-8')}".encode("utf-8"), client_socket)

        except:
            break

    # عند انقطاع الاتصال
    print(f"[SERVER LOG] {username} disconnected.")
    clients.remove(client_socket)
    usernames.remove(username)
    broadcast(f"{username} has left the chat.".encode("utf-8"))
    client_socket.close()

def start_server():
    """تشغيل السيرفر"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 5555))  # العنوان المحلي والمنفذ
    server_socket.listen()

    print("[SERVER STARTED] Server is running and listening on 127.0.0.1:5555 ...")

    while True:
        client_socket, addr = server_socket.accept()
        username = client_socket.recv(1024).decode("utf-8")
        usernames.append(username)
        clients.append(client_socket)

        print(f"[SERVER LOG] {username} connected from {addr}")

        broadcast(f"{username} has joined the chat!".encode("utf-8"))

        # تشغيل خيط جديد للتعامل مع المستخدم
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()

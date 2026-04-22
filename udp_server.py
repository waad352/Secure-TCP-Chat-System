import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 65433))

print("UDP Server is running and waiting for messages...")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode()

    print(f"Received from {addr}: {message}")

    if message.lower() == "exit":
        print("Client ended the chat.")
        server_socket.sendto("Goodbye!".encode(), addr)
        continue

    server_socket.sendto("Message received!".encode(), addr)
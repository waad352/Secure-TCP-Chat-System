import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 65433)

print("Type your message. Type 'exit' to quit.\n")

while True:
    message = input("You: ")

    client_socket.sendto(message.encode(), server_address)

    data, server = client_socket.recvfrom(1024)
    print("Server:", data.decode())

    if message.lower() == "exit":
        break

client_socket.close()
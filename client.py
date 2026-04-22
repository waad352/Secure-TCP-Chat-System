import socket
import sys

HOST = '127.0.0.1'
PORT = 65435

def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"❌ Connection failed! Please make sure the server is running on {HOST}:{PORT}.")
        sys.exit()
    except Exception as e:
        print(f"❌ Error during connection: {e}")
        sys.exit()

    try:
        username = input("Enter user name: ")
        if not username.strip():
            username = "Guest"
    except:
        username = "Guest"

    print(f"✅ Connected to the server as: {username}. Start chatting! Type 'exit' to quit.")

    while True:
        try:
            message = input(f"{username}: ")
            if message.lower() == 'exit':
                print("👋 Closing connection...")
                full_message = f"{username}: exit"
                client_socket.sendall(full_message.encode())
                break
            full_message = f"{username}: {message}"
            client_socket.sendall(full_message.encode())
            data = client_socket.recv(1024)
            if not data:
                print("⚠️ Server disconnected.")
                break
            print(f"Server: {data.decode()}")
        except KeyboardInterrupt:
            print("\n🛑 Client terminated by user.")
            break
        except ConnectionResetError:
            print("❌ Server closed the connection unexpectedly.")
            break
        except Exception as e:
            print(f"❌ Error occurred: {e}")
            break

    client_socket.close()
    print(" Socket closed.")

if __name__ == "__main__":
    start_client()
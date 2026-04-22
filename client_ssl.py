import socket
import ssl
import sys

HOST = '127.0.0.1'
PORT = 65432

def start_client():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        context = ssl.create_default_context()
        
        # Disable certificate verification for self-signed certificate testing
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)
        secure_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"❌ Connection failed! Make sure the server is running on {HOST}:{PORT}.")
        sys.exit()
    except Exception as e:
        print(f"❌ An error occurred during connection: {e}")
        sys.exit()

    print(f"✅ Secure connection established to the server on {HOST}:{PORT}.")
    print("Start chatting! Type 'exit' to quit.")

    while True:
        try:
            message = input("You: ")

            if not message.strip():
                continue

            if message.lower() == 'exit':
                print("👋 Closing connection...")
                secure_socket.sendall(message.encode('utf-8'))
                break

            secure_socket.sendall(message.encode('utf-8'))

            data = secure_socket.recv(1024)
            if not data:
                print("⚠️ Server disconnected.")
                break

            print(f"Server: {data.decode('utf-8')}")

        except KeyboardInterrupt:
            print("\n🛑 Client terminated by user.")
            break
        except ConnectionResetError:
            print("❌ Server unexpectedly reset the connection.")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            break

    secure_socket.close()
    print("🚪 Connection closed.")

if __name__ == "__main__":
    start_client()
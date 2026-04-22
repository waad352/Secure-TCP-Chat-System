import socket
import ssl
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

clients = []
client_count = 0

def handle_client(conn, addr, client_id):
    print(f"✅ Connection established from client {client_id} - Address: {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"🚫 Client {client_id} closed the connection.")
                break

            message = data.decode('utf-8').strip()
            print(f"💬 Client {client_id}: {message}")

            if message.lower() == 'exit':
                print(f"👋 Client {client_id} exited the chat.")
                break

            response = f"🔒 Your message was safely received: '{message}'"
            conn.sendall(response.encode('utf-8'))

    except ConnectionResetError:
        print(f"❌ Client {client_id} abruptly disconnected.")
    except Exception as e:
        print(f"⚠️ Error with client {client_id}: {e}")
    finally:
        conn.close()
        if conn in clients:
            clients.remove(conn)
        print(f"🚪 Connection closed with {addr}. Active clients: {len(clients)}")


def start_server():
    global client_count

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
    except Exception as e:
        print(f"❌ Failed to create or initialize the server: {e}")
        sys.exit()

    print(f"🟢 Server running on {HOST}:{PORT} using SSL...")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="server.key")

    try:
        while True:
            conn, addr = server_socket.accept()
            ssl_conn = context.wrap_socket(conn, server_side=True)

            client_count += 1
            clients.append(ssl_conn)

            thread = threading.Thread(target=handle_client, args=(ssl_conn, addr, client_count))
            thread.start()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped manually.")
    except Exception as e:
        print(f"⚠️ Error during connection acceptance: {e}")

    finally:
        for c in clients:
            c.close()
        server_socket.close()
        print("🔚 Server shut down.")


if __name__ == "__main__":
    start_server()

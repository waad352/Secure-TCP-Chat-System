import socket
import threading
import sys


HOST = '127.0.0.1'
PORT = 65435


clients = []
client_count = 0

def handle_client(conn, addr, client_id):

    client_display_name = f"Client {client_id}"
    print(f"✅ Connected by {client_display_name} from {addr}")
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"🚫 {client_display_name} has disconnected.")
                break
            
            full_message = data.decode()
            
            # 💡 تصحيح مسافة البداية (Indentation) هنا
            if ":" in full_message:
                parts = full_message.split(":", 1)
                client_display_name = parts[0].strip()  
                message_content = parts[1].strip()
            else:
                message_content = full_message
            
            print(f"{client_display_name} says: {message_content}")
            
            if message_content.lower() == 'exit':
                print(f"👋 {client_display_name} requested to exit.")
                break

            response = f"Message received'{message_content}'."
            conn.sendall(response.encode())

    except ConnectionResetError:
        print(f"❌ {client_display_name} connection closed unexpectedly.")
    except Exception as e:
        print(f"❌ Error with client {client_display_name}: {e}")
    finally:
        conn.close()
        if conn in clients: 
            clients.remove(conn)
        print(f"🚪 Connection with {addr} closed. Active clients: {len(clients)}")

def start_server():

    global client_count
    
  
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        server_socket.bind((HOST, PORT))
        server_socket.listen()
    except OSError as e:
        print(f"❌ Failed to create or bind a socket: {e}")
        sys.exit()
    except Exception as e:
        print(f"❌ General error during initialization: {e}")
        sys.exit()

    print(f"🟢 Server running on {HOST}:{PORT}...")

    while True:
        try:
           
            conn, addr = server_socket.accept()
            client_count += 1
            clients.append(conn)
            
            client_handler = threading.Thread(
                target=handle_client, 
                args=(conn, addr, client_count)
            )
            client_handler.start()
            
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user.")
            break
        except Exception as e:
            print(f"❌ Error while accepting connection: {e}")
            continueد
    server_socket.close()
    for conn in clients:
        conn.close()

if __name__ == "__main__":
    start_server()
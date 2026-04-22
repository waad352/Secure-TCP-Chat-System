# Secure-TCP-Chat-System
A robust Python-based communication system that demonstrates the implementation of **TCP/IP protocols**, **Multi-threading**, **SSL/TLS Encryption**, and **Graphical User Interfaces (GUI)**. This project was developed as part of my practical application in Network Security and Programming.
## 🚀 Features
* **Multi-Client Support:** Handles multiple simultaneous connections using Python's `threading` library.
* **Security (SSL/TLS):** Implements secure data transmission using SSL contexts and self-signed certificates to prevent eavesdropping.
* **User Interfaces:** Includes both Command Line Interface (CLI) and Graphical User Interface (GUI) versions using `Tkinter`.
* **Protocol Diversity:** Includes a basic UDP implementation for comparison between connection-oriented and connectionless protocols.

##  Project Structure
* `server.py` / `client.py`: Basic multi-threaded TCP chat.
* `server_ssl.py` / `client_ssl.py`: Secure version of the chat system using SSL/TLS.
* `server_gui.py` / `client_gui.py`: Interactive GUI version of the chat.
* `udp_server.py` / `udp_client.py`: Basic UDP communication scripts.
* `cert.pem` / `server.key`: Security credentials used for SSL encryption (for educational purposes).

## 🛠️ How to Run
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/waad352/Secure-TCP-Chat-System.git](https://github.com/waad352/Secure-TCP-Chat-System.git)
 2-  Run the Server:
python server_ssl.py
 3-Run the Client:
python client_ssl.py
Bash
python client_ssl.py
🔒 Security Note
The included server.key and cert.pem are self-signed certificates generated for testing and educational purposes only. In a production environment, certificates should be obtained from a trusted Certificate Authority (CA).
## Authors

** waad sultan 
 Suad suod 
 Atheer Taleb
 Shatha Ali 
 Aryam Alharbii**

# HiLCoE - School of Computer Science and Technology  
### CS662 - Advanced Computer Networking  
### Assignment II - Socket Programming 

---

## 👥 Group 7 Members:

    - Aman Fissehaye
    - Bethlehem Zebenay
    - Binyam Yeshitila
    - Eyob Melkamu
    - Orion Daniel
    - Tatek Habtegiorgis

---

# 🗨️ Multi-Client Chat Application in Python

This project is a simple multi-client chat application built using Python's `socket`, `tkinter` and `threading` modules. It demonstrates the fundamentals of socket programming by supporting both **TCP** and **UDP** protocols.

## 🔧 Features

- Real-time messaging between multiple clients.
- Server broadcasts messages to all connected clients.
- Username-based user identification.
- Graphical User Interface (GUI) built with Tkinter (for clients).
- Graceful handling of client disconnections and server shutdowns.

## ⚙️  Protocol Examples

### 🔌 TCP Version

- **TCP (Transmission Control Protocol)** provides reliable, connection-oriented communication.
- The server accepts multiple clients using threading.
- Each client establishes a persistent connection with the server.
- Messages are exchanged using `sendall()` and `recv()`.

### 📡 UDP Version

- **UDP (User Datagram Protocol)** provides fast, connectionless communication.
- The server listens for messages and keeps track of clients by their address.
- Clients send and receive messages using `sendto()` and `recvfrom()`.
- No persistent connection is established; more lightweight but less reliable than TCP.

## 🚀 How to Run

1. Start the server (`python tcp-server.py` or `python udp-server.py`).
2. Launch one or more clients (`python tcp-client.py` or `python udp-client.py`).
3. Enter a username and start chatting!

You can also run the executables in the [executables](./executables/) directory. Just start the server first then launch one or more clients.


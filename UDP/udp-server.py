#!/usr/bin/python3
"""UDP Server Script"""

import signal
import socket
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432
BUFFER_SIZE = 2048

clients = {}  # addr -> username
server_socket = None


def handle_new_message(data, addr):
    """Handles new messages"""

    message = data.decode("utf-8")

    if addr not in clients:
        clients[addr] = message
        broadcast_message(f"[SERVER] {message} has joined the chat.")
    else:
        full_message = f"{clients[addr]} ~ {message}"
        print(full_message)
        broadcast_message(full_message)


def broadcast_message(message: str):
    """Broadcastes messages to all clients"""

    for client_addr in clients:
        try:
            server_socket.sendto(message.encode("utf-8"), client_addr)  # pyright: ignore
        except Exception as e:
            print(f"[SERVER] Failed to send to {client_addr}: {e}")


def shutdown_server():
    """Handles server shutdown and disconnects all clients"""

    print("\n[SERVER] Shutting down...")
    broadcast_message("[SERVER] Server is shutting down.")
    if server_socket:
        server_socket.close()
    sys.exit(0)


def main():
    """Server main function"""

    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print(f"[SERVER] Running on {SERVER_IP}:{SERVER_PORT}")

    while True:
        try:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            handle_new_message(data, addr)
        except Exception as e:
            print(f"[SERVER] Error: {e}")


# Register signal handler
signal.signal(signal.SIGINT, lambda sig, frame: shutdown_server())

if __name__ == "__main__":
    main()

#!/usr/bin/python3
"""TCP server side script

---------------------------------------------
                HiLCoE
School of Computer Science and Technology
   CS662 - Advanced Computer Networks
---------------------------------------------


Group 7 Members:
   - Aman Fissehaye
   - Bethlehem Zebenay
   - Binyam Yeshitila
   - Eyob Melkamu
   - Orion Daniel
   - Tatek Habtegiorgis

"""

import signal
import sys
import threading
from socket import AF_INET, SOCK_STREAM, socket

SERVER_IP = "127.0.0.1"  # Standard loopback interface address (localhost)
SERVER_PORT = 65432  # Port to listen on, any non-privileged port > 1023 will do
LISTENER_LIMIT = 5  # Number of clients to litsen to concurrently
active_clients = []  # List of all connected users with the format (username, client)

# NOTE:
# Any client wanting to connect to this server must use the above IP address and port number


def remove_client(client: socket, username: str):
    """Remove a disconnected client from active_clients"""
    global active_clients
    active_clients = [(user, conn) for user, conn in active_clients if conn != client]

    try:
        client.close()
    except Exception as e:
        print(f"server ~ Error closing client socket: {e}")

    send_message_to_all(f"server ~ {username} has left the chat.")


def listen_for_messages(client: socket, username: str):
    """Function to listen for incoming messages from a client"""
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            if message:
                prompt_message = f"{username} ~ {message}"
                send_message_to_all(prompt_message)
            else:
                print(f"server ~ {username} has disconnected.")
                remove_client(client, username)
                break
        except Exception:
            print(f"server ~ Connection lost with {username}.")
            remove_client(client, username)
            break


def send_message_to_client(client: socket, message: str):
    """Function to send a message to a single client"""
    client.sendall(message.encode("utf-8"))


def send_message_to_all(message_sent: str):
    """Function to send any new messages to clients that are connected"""

    for user in active_clients:
        send_message_to_client(user[1], message_sent)


def client_handler(client: socket):
    """Function to handle client connections"""

    while True:
        # Server will listen for client message that will contain the username
        username = client.recv(2048).decode("utf-8")
        if username != "":
            active_clients.append((username, client))
            send_message_to_all(f"server ~ {username} has joined")
            break
        else:
            print("server ~ client username is empty")

    threading.Thread(
        target=listen_for_messages,
        args=(
            client,
            username,
        ),
    ).start()


def shutdown_server():
    """Handles server shutdown and disconnects all clients"""
    global active_clients, server

    print("server ~ Closing all client connections...")
    for username, client in active_clients:
        try:
            client.sendall("server ~ Server is shutting down.".encode("utf-8"))
            client.close()
        except Exception as e:
            print(f"server ~ Error closing client {username}: {e}")

    active_clients.clear()  # Remove all clients from the list

    try:
        server.close()
        print("server ~ Server socket closed.")
    except Exception as e:
        print(f"server ~ Error closing server socket: {e}")

    sys.exit(0)  # Exit the program cleanly


def main():
    """Server main function"""
    global server  # Declare server as global so we can close it in signal handler

    server = socket(AF_INET, SOCK_STREAM)

    try:
        server.bind((SERVER_IP, SERVER_PORT))
        print(f"server ~ Running the server @{SERVER_IP}:{SERVER_PORT}")
    except Exception as e:
        print(f"server ~ Unable to bind server @{SERVER_IP}:{SERVER_PORT}")
        print(f"server ~ {e}")
        sys.exit(1)  # Exit if binding fails

    server.listen(LISTENER_LIMIT)

    print("server ~ Waiting for connections... (Press Ctrl+C to stop)")

    try:
        while True:
            client, address = server.accept()
            print(f"server ~ Successfully connected to client @{address[0]}:{address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()
    except KeyboardInterrupt:
        print("\nserver ~ Shutting down gracefully...")
        shutdown_server()


# Handle Ctrl+C shutdown
signal.signal(signal.SIGINT, lambda sig, frame: shutdown_server())

if __name__ == "__main__":
    main()

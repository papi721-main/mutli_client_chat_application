#!/usr/bin/python3
"""TCP Sever Script"""

import threading
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket

SERVER_IP = "127.0.0.1"  # Standard loopback interface address (localhost)
SERVER_PORT = 65432  # Port to listen on, any non-privileged port > 1023 will do
LISTENER_LIMIT = 5  # Number of clients to litsen to concurrently
active_clients = []  # List of all connected users with the format (username, client)

# NOTE:
# Any client wanting to connect to this server must use the above IP address
# and port number


def listen_for_messages(client: socket, username: str):
    """Function to listen for upcoming messages from a client"""

    while True:
        message = client.recv(2048).decode("utf-8")
        if message != "":
            # Craft the final message displayed and send that to all clients
            final_message = f"{username} ~ {message}"
            send_message_to_all(username, final_message)
        else:
            print(f"The message sent from the client {username} is empty")
            exit(0)


def send_message_to_client(client: socket, message: str):
    """Function to send a message to a single client"""
    client.sendall(message.encode("utf-8"))


def send_message_to_all(sender_username: str, message_sent: str):
    """Function to send any new messages to clients that are connected"""

    for user in active_clients:
        # NOTE:
        # user[0] = client username
        # user[1] = client socket object
        if user[0] != sender_username:  # send the message to all users except the sender
            send_message_to_client(user[1], message_sent)


def client_handler(client: socket):
    """Function to handle client connections"""

    while True:
        # Server will listen for client message that will contain the username
        username = client.recv(2048).decode("utf-8")
        if username != "":
            active_clients.append((username, client))
            send_message_to_all(username, f"SERVER ~ {username} has joined")
            break
        else:
            print("Server ~ client username is empty")

    threading.Thread(
        target=listen_for_messages,
        args=(
            client,
            username,
        ),
    ).start()


def main():
    """Server main function"""

    # NOTE:
    # AF_INET = Internet Address family for IPv4
    # SOCK_STREAM = socket type for TCP connection

    with socket(AF_INET, SOCK_STREAM) as server:
        # Bind the server with a host ip address and port number
        try:
            server.bind((SERVER_IP, SERVER_PORT))
        except Exception as e:
            print(f"Server ~ Unable to bind server at IP: {SERVER_IP} PORT: {SERVER_PORT}")
            print(f"Server ~ Error Message: {e}")

        # Set server limit
        server.listen(LISTENER_LIMIT)

        # Now this while loop makes sure the server keeps on listening for a
        # client connection request
        while True:
            # server.accept() blocks execution and waits for incoming connections
            client, address = server.accept()

            print(
                f"Server ~ Successfully connected to client at ip: {address[0]}, port: {address[1]}"
            )

            threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == "__main__":
    main()

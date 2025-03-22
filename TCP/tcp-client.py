#!/usr/bin/python3
"""TCP Client Script"""
import threading
import tkinter as tk
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket

root = tk.Tk()  # Get a Tkinter window object
root.geometry("600x600")  # Set the size of the Tkinter window
root.title("Messenger Client")  # Set the title of the window
root.resizable(False, False)  # Disable window resizablity for width and height

# GUI constants
DARK_GREY = "#121212"
MEDIUM_GREY = "#1F1B24"
OCEAN_BLUE = "#464EB8"
FONT = ("Helvetica", 17)
SMALL_FONT = ("Helvetica", 13)

# Socket constants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432


def listen_for_messages_from_server(client: socket):
    """Function to listen for messages from server"""

    while True:
        message = client.recv(2048).decode("utf-8")
        if message != "":
            # username = message.split(" ~ ")[0]
            # content = message.split(" ~ ")[1]
            print(message)
        else:
            # print("Message recieved from server is empty")
            print()


def send_message_to_server(client: socket):
    """Function for sending messages to client"""

    while True:
        message = input()
        if message != "":
            client.sendall(message.encode("utf-8"))
        else:
            print("Empty message")
            exit(0)


def communicate_to_server(client: socket):
    """Function to communicate with the server"""

    username = input("Enter username: ")
    if username != "":
        client.sendall(username.encode("utf-8"))  # Send the username to the server
    else:
        print("Username can not be empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    send_message_to_server(client)


def main():
    """Client main function"""

    # Start the tkinter GUI window
    root.mainloop()

    with socket(AF_INET, SOCK_STREAM) as client:

        try:
            # Connect to the server
            client.connect((SERVER_IP, SERVER_PORT))
        except Exception as e:
            print(f"Unable to connect to server at IP: {SERVER_IP} PORT: {SERVER_PORT}")
            print(f"Error Message: {e}")

        communicate_to_server(client)


if __name__ == "__main__":
    main()

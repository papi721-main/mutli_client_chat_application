#!/usr/bin/python3
"""TCP Client Script"""
import threading
import tkinter as tk
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
from tkinter import messagebox, scrolledtext

# GUI constants
DARK_GREY = "#121212"
MEDIUM_GREY = "#1F1B24"
OCEAN_BLUE = "#464EB8"
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Socket constants
SERVER_IP = "127.0.0.1"
SERVER_PORT = 65432

# Create the client socket object
client = socket(AF_INET, SOCK_STREAM)


def add_message(message: str):
    """Function to write messages on the GUI"""

    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    message_box.config(state=tk.DISABLED)


def connect_to_server():
    """Function to connect with the server"""

    try:
        print("Trying to connect")
        # Connect to the server
        client.connect((SERVER_IP, SERVER_PORT))
        # client_address = client.recv(2048).decode("utf-8")
        print("Successfully connected to the server")
        add_message("[SERVER] Successfully connected to the server")
    except Exception as e:
        messagebox.showerror(
            title="Connection Error",
            message=f"Unable to connect to server at {SERVER_IP}:{SERVER_PORT}\n\n{e}",
        )

    username = username_textbox.get()
    print(username + " recieved")
    if username != "":
        client.sendall(username.encode("utf-8"))  # Send the username to the server
        # main_window.title(f"{username} @{client_address}")
        main_window.title(f"{username}")
    else:
        messagebox.showerror(
            title="Invalid username",
            message=f"Username cannot be empty",
        )

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    """Function for sending messages in the GUI"""

    message = message_textbox.get()
    print(message)
    if message != "":
        client.sendall(message.encode("utf-8"))
        message_textbox.delete(0, len(message))
        print(message + " is sent")
    else:
        messagebox.showerror(title="Empty message", message="Message cannot be empty")


def listen_for_messages_from_server(client: socket):
    """Function to listen for messages from the server"""

    while True:
        message = client.recv(2048).decode("utf-8")
        if message != "":
            # username = message.split(" ~ ")[0]
            # content = message.split(" ~ ")[1]
            add_message(message)
        else:
            messagebox.showerror(title="Error", message="Message recevied from client is empty")


# Build the GUI
main_window = tk.Tk()  # Get a Tkinter window object
main_window.geometry("600x600")  # Set the size of the Tkinter window
main_window.title("Messenger Client")  # Set the title of the window
main_window.resizable(False, False)  # Disable window resizing for width and height

# Create the top, middle and bottom frames
top_frame = tk.Frame(main_window, width=600, height=100, bg=DARK_GREY)
middle_frame = tk.Frame(main_window, width=600, height=400, bg=MEDIUM_GREY)
bottom_frame = tk.Frame(main_window, width=600, height=100, bg=DARK_GREY)

# Position the frames
top_frame.grid(row=0, column=0, sticky=tk.NSEW)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# Adjust the height of the frames
main_window.grid_rowconfigure(0, weight=1)  # Top frame
main_window.grid_rowconfigure(1, weight=4)  # Middle Frame
main_window.grid_rowconfigure(2, weight=1)  # Bottom Frame

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(
    top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect_to_server
)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(
    bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message
)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(
    middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5
)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


# Main Program Function
def main():
    """Client main function"""

    # Start the client GUI
    main_window.mainloop()


if __name__ == "__main__":
    main()

#!/usr/bin/python3
"""TCP Client Script

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
import threading
import tkinter as tk
from socket import AF_INET, SOCK_STREAM, socket, timeout
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
client.settimeout(1)  # Set timeout to prevent blocking

stop_threads = False  # Global flag to stop threads


def display_message(message: str):
    """Function to write messages on the GUI"""

    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + "\n")
    message_box.config(state=tk.DISABLED)


def connect_to_server():
    """Function to connect with the server"""

    global stop_threads
    stop_threads = False  # Reset flag in case of reconnection

    try:
        client.connect((SERVER_IP, SERVER_PORT))
        display_message("server ~ Successfully connected to the server")
    except Exception as e:
        messagebox.showerror(
            title="Connection Error",
            message=f"Unable to connect to server at {SERVER_IP}:{SERVER_PORT}\n\n{e}",
        )
        return

    username = username_textbox.get()
    if username:
        client.sendall(username.encode("utf-8"))
        main_window.title(f"{username}")
    else:
        messagebox.showerror(title="Invalid username", message="Username cannot be empty")
        return

    threading.Thread(target=listen_for_messages_from_server, daemon=True).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    """Function for sending messages in the GUI"""

    message = message_textbox.get()
    if message:
        try:
            client.sendall(message.encode("utf-8"))
            message_textbox.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Failed to send message: {e}")
    else:
        messagebox.showerror(title="Empty message", message="Message cannot be empty")


def listen_for_messages_from_server():
    """Function to listen for messages from the server"""

    global stop_threads
    while not stop_threads:
        try:
            message = client.recv(2048).decode("utf-8")
            if message:
                display_message(message)
        except timeout:
            continue  # Prevent blocking when stopping threads
        except Exception:
            break  # Exit thread when socket is closed


def on_closing():
    """Handle window closing event."""

    global stop_threads
    stop_threads = True  # Stop the listening thread

    try:
        client.shutdown(2)  # Shut down both send and receive operations
        client.close()  # Close the socket connection
    except Exception as e:
        print(f"Error closing socket: {e}")

    main_window.destroy()  # Close the Tkinter window


# Build the GUI
main_window = tk.Tk()
main_window.geometry("600x600")
main_window.title("Messenger Client")
main_window.resizable(False, False)

# Bind the close event
main_window.protocol("WM_DELETE_WINDOW", on_closing)

# Create the GUI layout
top_frame = tk.Frame(main_window, width=600, height=100, bg=DARK_GREY)
middle_frame = tk.Frame(main_window, width=600, height=400, bg=MEDIUM_GREY)
bottom_frame = tk.Frame(main_window, width=600, height=100, bg=DARK_GREY)

top_frame.grid(row=0, column=0, sticky=tk.NSEW)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

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

# Run the Tkinter main loop
main_window.mainloop()

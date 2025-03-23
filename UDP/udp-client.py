#!/usr/bin/python3
"""UDP Client Script

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
from socket import AF_INET, SOCK_DGRAM, socket
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

client = socket(AF_INET, SOCK_DGRAM)
client.settimeout(1)
username = ""
stop_threads = False


def add_message(message: str):
    """Function to write messages on the GUI"""
    message_box.config(state=tk.NORMAL)

    message_box.insert(tk.END, message + "\n")
    message_box.config(state=tk.DISABLED)


def connect_to_server():
    """Function to connect with the server"""

    global username, stop_threads
    stop_threads = False

    username = username_textbox.get()
    if username:
        client.sendto(username.encode("utf-8"), (SERVER_IP, SERVER_PORT))
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
            client.sendto(message.encode("utf-8"), (SERVER_IP, SERVER_PORT))
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
            data, _ = client.recvfrom(2048)
            add_message(data.decode("utf-8"))
        except Exception as _:
            continue


def on_closing():
    """Handle window closing event."""

    global stop_threads
    stop_threads = True
    client.close()
    main_window.destroy()


# GUI setup
main_window = tk.Tk()
main_window.geometry("600x600")
main_window.title("Messenger Client")
main_window.resizable(False, False)
main_window.protocol("WM_DELETE_WINDOW", on_closing)

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

main_window.mainloop()

# Python Console-Based Chat Application

## Description

This project is a simple, console-based (command-line interface) chat application built from scratch using Python. It serves as an educational tool to demonstrate core networking concepts, client-server architecture, multi-threading for handling multiple users, basic message exchange, and a simple implementation of message encryption.

The application allows multiple clients to connect to a central server, send messages that are broadcast to all other connected clients, and see messages from others in real-time, all within the console.

## Features

* **Client-Server Architecture:** Uses TCP sockets for reliable communication.
* **Multi-User Support:** The server can handle multiple clients concurrently using threading.
* **Message Broadcasting:** Messages sent by one client are broadcast to all other connected clients.
* **User Identification:** Clients can set a nickname upon connecting, which is displayed with their messages.
* **Simple Message Encryption:** Implements a basic Caesar cipher for encrypting messages between clients (relayed through the server). This is for educational purposes only and not secure for real-world use.
* **Graceful Exit:** Clients can disconnect using a `/quit` command, and basic error handling is in place.
* **Console-Based Interface:** All interactions happen via the command line.

## Technologies Used

* **Python 3.x**
* Standard Python Libraries:
    * `socket` (for network connections)
    * `threading` (for concurrency)
    * `sys` (for system-specific parameters and functions)

## Setup and Prerequisites

* Ensure you have Python 3.6 or newer installed on your system.
* No external libraries beyond the Python standard library are required for the core functionality using the Caesar cipher.

## How to Run

1.  **Clone the repository or download the files.**
    ```bash
    # If you have git installed
    # git clone <your-repository-url>
    # cd <repository-name>
    ```
    Otherwise, ensure `basic_server.py`, `basic_client.py`, and `simple_crypto.py` are in the same directory.

2.  **Start the Server:**
    Open a terminal or command prompt, navigate to the project directory, and run:
    ```bash
    python3 basic_server.py
    ```
    The server will start and print messages indicating it's bound to an address (e.g., `127.0.0.1:55555`) and listening for connections.

3.  **Start one or more Clients:**
    Open a *new* terminal window for *each* client you want to run. Navigate to the project directory and run:
    ```bash
    python3 basic_client.py
    ```
    * Each client will prompt you to enter a nickname.
    * After entering a nickname, you can start sending and receiving messages.
    * Type `/quit` in a client window to disconnect that client.

## File Structure

* `basic_server.py`: Contains the logic for the chat server.
* `basic_client.py`: Contains the logic for the chat client.
* `simple_crypto.py`: Contains the Caesar cipher encryption and decryption utility functions.
* `README.md`: This documentation file.

## Core Concepts Demonstrated

This project illustrates several fundamental programming and networking concepts:
* Socket programming (TCP/IP)
* Client-Server model
* Multi-threading for concurrent client handling (server-side)
* Multi-threading for non-blocking UI (client-side send/receive)
* Basic data encoding/decoding (UTF-8)
* Implementation of a simple symmetric encryption algorithm (Caesar cipher)
* Resource management (e.g., ensuring sockets are closed)
* Basic error handling in network applications

## Limitations & Disclaimer

* **Educational Purposes Only:** This application was built as a learning exercise.
* **Basic Encryption:** The Caesar cipher implemented is **not secure** and should not be used for sensitive information or real-world applications. It is included purely to demonstrate the mechanism of encryption.
* **Console UI:** The user interface is entirely text-based in the console.
* **Limited Error Handling:** While basic error handling is included, production applications would require more comprehensive and robust error management.
* **No Persistent Storage:** Chat messages and user information are not saved and are lost when the server or clients are closed.

## Potential Future Enhancements

* **Graphical User Interface (GUI):** Using libraries like Tkinter, PyQt, or Kivy.
* **Stronger Encryption:** Implementing more secure encryption algorithms (e.g., AES via the `cryptography` library) and secure key exchange mechanisms.
* **Private Messaging:** Allowing users to send direct messages to specific individuals.
* **Chat Rooms/Channels:** Support for multiple chat rooms.
* **User Authentication:** A more robust system for user login and registration.
* **Asynchronous I/O:** Using `asyncio` for potentially more efficient handling of many connections.

---

Feel free to customize this README further. For example, you might want to add a section about yourself as the author, a license (like MIT if you want to make it open source), or more specific details if you add more features.

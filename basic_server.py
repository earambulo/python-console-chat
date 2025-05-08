# basic_server.py
import socket
import threading
from simple_crypto import caesar_encrypt, caesar_decrypt # Import encryption functions

HOST = '127.0.0.1'
PORT = 55555
SHARED_SHIFT_KEY = 3 # Must be the same in the client

clients_info = {} # socket: nickname
clients_lock = threading.Lock()

def broadcast_message(encrypted_message_bytes, sender_socket_for_exclusion=None):
    with clients_lock:
        active_sockets = list(clients_info.keys())
    
    for client_socket in active_sockets:
        # if sender_socket_for_exclusion and client_socket == sender_socket_for_exclusion:
        # continue
        try:
            client_socket.sendall(encrypted_message_bytes)
        except socket.error:
            print(f"[!] Error sending to a client during broadcast (it may have disconnected).")

def handle_client(conn_socket, addr):
    thread_name = threading.current_thread().name
    print(f"[*] New connection from {addr[0]}:{addr[1]} on thread: {thread_name}")
    
    nickname = None
    try:
        # Nickname is received in PLAINTEXT
        nickname_bytes = conn_socket.recv(1024)
        if not nickname_bytes:
            print(f"[!] Client {addr} disconnected before sending nickname.")
            return
        
        nickname = nickname_bytes.decode('utf-8').strip()
        if not nickname:
            print(f"[!] Client {addr} sent an empty nickname. Disconnecting.")
            # Send an encrypted error message
            error_msg_plain = "[SERVER] Nickname cannot be empty. Disconnecting."
            error_msg_encrypted = caesar_encrypt(error_msg_plain, SHARED_SHIFT_KEY)
            conn_socket.sendall(error_msg_encrypted.encode('utf-8'))
            return

        with clients_lock:
            clients_info[conn_socket] = nickname
        print(f"[*] Nickname '{nickname}' set for {addr}. Total clients: {len(clients_info)}")
        
        # Announce new user (ENCRYPTED)
        welcome_message_plain = f"[SERVER] '{nickname}' has joined the chat!"
        welcome_message_encrypted = caesar_encrypt(welcome_message_plain, SHARED_SHIFT_KEY)
        broadcast_message(welcome_message_encrypted.encode('utf-8'))

        # Handle Regular Messages (which will be encrypted by client)
        while True:
            # Expecting encrypted message bytes from client
            encrypted_data_from_client = conn_socket.recv(1024) # This is ENCRYPTED
            if encrypted_data_from_client:
                # Server relays the encrypted data directly.
                # For logging, server could decrypt if it wanted to, but we're keeping it simple.
                # print(f"[*] Received ENCRYPTED from '{nickname}': {encrypted_data_from_client.decode('utf-8')[:30]}...") # Log snippet
                
                broadcast_message(encrypted_data_from_client) # Broadcast the still-encrypted bytes
            else:
                print(f"[*] '{nickname}' ({addr}) disconnected gracefully (empty data).")
                break
    except socket.error as e:
        if nickname: print(f"[!] Socket error with '{nickname}' ({addr}): {e}")
        else: print(f"[!] Socket error with {addr} before nickname set: {e}")
    except UnicodeDecodeError: # Might happen if client sends non-UTF8 nickname
        print(f"[!] UnicodeDecodeError from '{nickname if nickname else addr}'.")
    finally:
        with clients_lock:
            removed_nickname = clients_info.pop(conn_socket, None)

        if removed_nickname:
            print(f"[*] Client '{removed_nickname}' ({addr}) removed. Total clients: {len(clients_info)}")
            # Announce user leaving (ENCRYPTED)
            disconnect_message_plain = f"[SERVER] '{removed_nickname}' has left the chat."
            disconnect_message_encrypted = caesar_encrypt(disconnect_message_plain, SHARED_SHIFT_KEY)
            broadcast_message(disconnect_message_encrypted.encode('utf-8'))
        else:
            print(f"[*] Client {addr} (no nickname set) removed. Total clients: {len(clients_info)}")
            
        conn_socket.close()
        print(f"[*] Connection with {addr} ({thread_name}) closed.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((HOST, PORT))
        print(f"[*] Socket bound to {HOST}:{PORT}")
    except socket.error as e:
        print(f"[!] Bind failed: {e}"); server_socket.close(); exit()

    server_socket.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}...")
    try:
        while True:
            conn_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn_socket, addr), daemon=True)
            client_thread.start()
            with clients_lock:
                 print(f"[*] Active client handler threads (approx): {threading.active_count() - 1}, Connected clients in dict: {len(clients_info)}")
    except KeyboardInterrupt: print("\n[*] Server is shutting down...")
    finally:
        shutdown_msg_plain = "[SERVER] Server is shutting down. You will be disconnected."
        shutdown_msg_encrypted = caesar_encrypt(shutdown_msg_plain, SHARED_SHIFT_KEY)
        with clients_lock:
            active_sockets = list(clients_info.keys())
            for client_socket in active_sockets:
                try:
                    client_socket.sendall(shutdown_msg_encrypted.encode('utf-8'))
                    client_socket.close()
                except socket.error: pass 
        server_socket.close()
        print("[*] Server socket closed.")

if __name__ == "__main__":
    start_server()
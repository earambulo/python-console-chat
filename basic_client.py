# basic_client.py
import socket
import threading
import sys
from simple_crypto import caesar_encrypt, caesar_decrypt # Import encryption functions

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 55555
SHARED_SHIFT_KEY = 3 # Must be the same in the server

stop_event = threading.Event()
client_nickname = "" # Store client's nickname globally for prepending

def receive_messages(client_socket):
    while not stop_event.is_set():
        try:
            encrypted_message_bytes = client_socket.recv(1024)
            if not encrypted_message_bytes:
                print("\n[*] Server has closed the connection. Press Enter to exit.")
                stop_event.set()
                client_socket.close()
                break
            
            encrypted_message = encrypted_message_bytes.decode('utf-8')
            decrypted_message = caesar_decrypt(encrypted_message, SHARED_SHIFT_KEY) # DECRYPT HERE
            
            sys.stdout.write(f"\r{decrypted_message}\n> ")
            sys.stdout.flush()
        except socket.error:
            if not stop_event.is_set():
                print(f"\n[!] Error receiving message. Disconnecting.")
                stop_event.set()
            client_socket.close()
            break
        except UnicodeDecodeError: # Could happen if trying to decode non-UTF-8 before decryption
            if not stop_event.is_set():
                print("\n[!] Error decoding message from server (prior to decryption).")
        except Exception as e: # Catch other potential errors during decryption
             if not stop_event.is_set():
                print(f"\n[!] Error processing received message: {e}")


def send_messages(client_socket):
    global client_nickname # Access the nickname
    sys.stdout.write("> ")
    sys.stdout.flush()

    while not stop_event.is_set():
        try:
            message_to_send = sys.stdin.readline().strip()
            if stop_event.is_set():
                break
            
            if message_to_send:
                if message_to_send.lower() == '/quit':
                    print("[*] Disconnecting...")
                    stop_event.set()
                    # /quit message itself won't be encrypted as we're closing
                    client_socket.close()
                    break
                
                # Prepend nickname and then encrypt
                formatted_message = f"[{client_nickname}]: {message_to_send}"
                encrypted_message = caesar_encrypt(formatted_message, SHARED_SHIFT_KEY) # ENCRYPT HERE
                
                client_socket.sendall(encrypted_message.encode('utf-8'))
                sys.stdout.write("> ")
                sys.stdout.flush()
        except (socket.error, OSError):
            if not stop_event.is_set():
                print(f"\n[!] Error sending message. Connection lost.")
                stop_event.set()
            client_socket.close()
            break
        except KeyboardInterrupt:
            print("\n[*] Quitting via Ctrl+C...")
            stop_event.set()
            client_socket.close()
            break
    print("[*] Exiting send message loop.")


def start_client():
    global client_nickname # To set it after input
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[*] Client socket created.")

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[*] Connected successfully to {SERVER_HOST}:{SERVER_PORT}")

        while True:
            nickname_input = input("Enter your nickname: ").strip()
            if nickname_input:
                client_nickname = nickname_input # Store for later use
                # Nickname is sent in PLAINTEXT
                client_socket.sendall(client_nickname.encode('utf-8'))
                print(f"[*] Nickname '{client_nickname}' sent to server.")
                break
            else:
                print("[!] Nickname cannot be empty. Please try again.")

        receiver_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        receiver_thread.start()
        send_messages(client_socket)

    except socket.error as e:
        print(f"[!] Failed to connect or communicate with server: {e}")
    except KeyboardInterrupt:
        print("\n[*] Client startup interrupted by user. Exiting.")
    finally:
        stop_event.set()
        if hasattr(client_socket, 'fileno') and client_socket.fileno() != -1:
            client_socket.close()
        print("[*] Client has shut down.")
        if 'receiver_thread' in locals() and receiver_thread.is_alive():
            receiver_thread.join(timeout=1.0)
        print("[*] All client threads terminated.")

if __name__ == "__main__":
    start_client()
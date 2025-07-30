import socket
import threading

# Receive messages from server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Connection closed by server.")
            sock.close()
            break

# Main client function
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("127.0.0.1", 8080))  # Connect to server on localhost
    except:
        print("Failed to connect to server.")
        return

    name = input("Enter your name: ")

    # Start receiver thread
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    # Send messages
    while True:
        message = input()
        if message.lower() == "exit":
            break
        client.send(f"{name}: {message}".encode())

    client.close()

if __name__ == "__main__":
    start_client()
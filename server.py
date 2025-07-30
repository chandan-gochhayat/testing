import socket
import threading

clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"{addr}: {message.decode()}")
            broadcast(message, client_socket)
        except Exception as e:
            print(f"[ERROR] Client {addr} caused an exception: {e}")
            break

    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen()

    print("[STARTED] Chat server is running on port 8080...")

    while True:
        client_socket, addr = server.accept()
        with clients_lock:
            clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

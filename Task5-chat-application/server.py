import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def broadcast(message, client_socket=None):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(500000).decode()
            if not message:
                break
            broadcast(message, client)
        except:
            break

    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        broadcast(f"TEXT::{username} left the chat.")
        clients.remove(client)
        usernames.remove(username)

    client.close()

def receive():
    print(f"Server running on {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")

        username = client.recv(1024).decode()
        clients.append(client)
        usernames.append(username)

        broadcast(f"TEXT::{username} joined the chat.")

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()

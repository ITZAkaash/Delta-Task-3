import socket
import zlib
import hashlib
import random

def compress_file(filename):
    with open(filename, "rb") as f:
        data = f.read()
    compressed_data = zlib.compress(data)
    return compressed_data

def decompress_file(compressed_data):
    data = zlib.decompress(compressed_data)
    return data

def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(5)
    print("Server is listening on port", port)
    users = {
        "username1": "password1",
        "username2": "password2",
    }
    while True:
        client_socket, address = server_socket.accept()
        print("Client connected from", address)
        data = client_socket.recv(1024)
        if data == b"login":
            username = client_socket.recv(1024).decode()
            password = client_socket.recv(1024).decode()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if username in users and hashed_password == users[username]:
                client_socket.sendall(b"success")
            else:
                client_socket.sendall(b"fail")
        elif data == b"upload":
            filename = client_socket.recv(1024).decode()
            compressed_data = client_socket.recv(1024)
            file_name = "{}.zip".format(filename)
            with open(file_name, "wb") as f:
                f.write(compressed_data)
            client_socket.sendall(b"File stored as {}".format(file_name))
        elif data == b"download":
            filename = client_socket.recv(1024).decode()
            if filename in users:
                with open(filename, "rb") as f:
                    compressed_data = f.read()
                client_socket.sendall(compressed_data)
        client_socket.close()

def client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server")
    client_socket.sendall(b"login")
    username = input("Enter username: ")
    client_socket.sendall(username.encode())
    password = input("Enter password: ")
    client_socket.sendall(password.encode())
    response = client_socket.recv(1024)
    if response == b"success":
        print("Login successful")
        client_socket.sendall(b"upload")
        filename = input("Enter file name: ")
        client_socket.sendall(filename.encode())
        compressed_data = compress_file(filename)
        client_socket.sendall(compressed_data)
        print("File uploaded")
        client_socket.sendall(b"download")
        filename = input("Enter file name to download: ")
        client_socket.sendall(filename.encode())
        compressed_data = client_socket.recv(1024)
        data = decompress_file(compressed_data)
        with open(filename, "wb") as f:
            f.write(data)
        print("File downloaded")
    else:
        print("Login failed")

if _name_ == "_main_":
    port = 8080
    server(port)
    # or
    # client("localhost", port)
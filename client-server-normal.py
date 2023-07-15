import socket
import zlib

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8080))
server_socket.listen(1)

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()

    # Receive the file name
    filename = client_socket.recv(1024).decode()

    # Open the file
    with open(filename, "rb") as f:
        data = f.read()

    # Compress the data
    compressed_data = zlib.compress(data)

    # Send the file name and compressed data to the client
    client_socket.send(filename.encode())
    client_socket.sendall(compressed_data)

    # Close the client connection
    client_socket.close()


# Create a client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8080))

# Send the file name to the server
client_socket.send("dummy.txt".encode())

# Receive the file name and compressed data from the server
filename = client_socket.recv(1024).decode()
compressed_data = client_socket.recv(1024)

# Decompress the data
decompressed_data = zlib.decompress(compressed_data)

# Save the data to a file
with open(filename, "wb") as f:
    f.write(decompressed_data)

# Close the client connection
client_socket.close()
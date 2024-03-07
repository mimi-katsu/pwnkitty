import socket

def start_server(host='0.0.0.0', port=4444):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")

        while True:  # Keep the server running
            client_socket, addr = server_socket.accept()  # Accept a new connection
            print(f"Connection from {addr}")

            with client_socket:  # Automatically close the client socket when done
                
                while True:
                    command = input(">:")
                    client_socket.sendall((command + "\n").encode())
                    data = client_socket.recv(1024)  # Receive data from the client
                    if not data:
                        break  # If no data is received, it means the client has closed the connection
                    print(f"Received: {data.decode()}")  # Print the received data
                    
                    # Optionally, you can send data back to the client
                    # client_socket.sendall(b"Response from server")

            print("Connection closed")

if __name__ == "__main__":
    start_server()
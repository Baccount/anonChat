import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9050))
client_socket.send(input("Enter your username: ").encode("utf-8"))


while True:
    message = client_socket.recv(4096).decode("utf-8")
    if not message:
        print("Server is down. You are now disconnected.")
        break
    print(message)
    client_socket.send(input().encode("utf-8"))

client_socket.close()

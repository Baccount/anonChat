import socket
import select
from stem.control import Controller

port = 8010
controller = Controller.from_port(port = 9051)
controller.authenticate()

# Create a new hidden service
response = controller.create_ephemeral_hidden_service({80: port}, await_publication = True)
print("Hostname (onion address): %s" % response.service_id + ".onion")

# Start the hidden service
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", port))
server.listen()

sockets_list = [server]
clients = {}






def bounce_message(message):
    # send message to all clients except the sender
    for client_socket in clients:
        if client_socket != notified_socket:
            client_socket.send(f"{user}: {message}".encode("utf-8"))






def receive_message(client_socket):
    try:
        message = client_socket.recv(4096).decode("utf-8")
        return message
    except Exception as e:
        print(f"Error: {e}")
        return False

while True:
    try:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server:
                client_socket, client_address = server.accept()
                user = receive_message(client_socket)
                if user is False:
                    continue
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print(f"Accepted new connection username:{user}")
            else:
                message = receive_message(notified_socket)
                # empty message means the client disconnected
                if message is False or message == "":
                    print(f"Closed connection from {clients[notified_socket]}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                user = clients[notified_socket]
                print(f"Received message from {user}: {message}")
                # send message to all clients
                bounce_message(message)
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
    except KeyboardInterrupt:
        print("Server is shutting down...")
        # close all connections
        for client_socket in clients:
            client_socket.close()
        # close tor connection
        controller.close()
        # close server socket
        server.close()
        exit()
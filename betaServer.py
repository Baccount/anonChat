import socket
import select
from stem.control import Controller
from random import randint
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%I:%M:%S %p')

log = logging.getLogger(__name__)





port = randint(10000, 65535)
log.debug(f"Randomly generated port: {port}")

controller = Controller.from_port(port = 9051)
controller.authenticate()
log.debug(f"Connected to Tor control port: {controller.get_info('version')}")

# Create a new hidden service
response = controller.create_ephemeral_hidden_service({80: port}, await_publication = True)
log.debug(f"Created new hidden service with onion address: {response.service_id}.onion")
try:
    # Start the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", port))
    server.listen()
except ConnectionResetError:
    print("Connection reset error")
    server.close()
    exit()


sockets_list = [server]
clients = {}






def bounce_message(message, notified_socket, user):
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


def start_server():
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
                    bounce_message(message, notified_socket, user)
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




if __name__ == "__main__":
    start_server()
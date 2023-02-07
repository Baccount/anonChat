import stem
import stem.connection
from stem import Signal
from stem.control import Controller
import socket

# Define the port number to listen on
port = 8010

def create_onion_service():
  with Controller.from_port(port = 9051) as controller:
    controller.authenticate()

    # Create a new hidden service
    response = controller.create_ephemeral_hidden_service({80: port}, await_publication = True)
    print("Hostname (onion address): %s" % response.service_id + ".onion")

    # Start the hidden service
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", port))
    sock.listen(1)

    # Wait for incoming connections
    print("Listening for incoming connections...")
    while True:
      conn, addr = sock.accept()
      data = conn.recv(1024)
      print("Received message: %s" % data)
      message = input("Enter your response: ")
      conn.send(message.encode())

create_onion_service()

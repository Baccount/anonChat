import stem
import stem.connection
from stem import Signal
from stem.control import Controller
import socket
# import sleep
from time import sleep

# Define the port number to listen on
port = 8010

def create_onion_service(debug = False):
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()

        # Create a new hidden service
        response = controller.create_ephemeral_hidden_service({80: port}, await_publication = True)
        print("Hostname (onion address): %s" % response.service_id + ".onion")

        # Start the hidden service
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", port))
        sock.listen(20)








        print("Listening for incoming connections...")
        try:
            # handle connection drop
            conn, addr = sock.accept()
            while True:
                data = conn.recv(1024)
                print("Received: %s" % data.decode())
                conn.send(data)
                print(data)




















        except KeyboardInterrupt:
            # close the socket
            print("Closing socket...")
            controller.remove_ephemeral_hidden_service(response.service_id)
            sock.close()
        except Exception as e:
            print(e)
        finally:
            # close the socket
            print("Closing socket...")
            controller.remove_ephemeral_hidden_service(response.service_id)
            sock.close()



def main():
    create_onion_service(debug = True)


if __name__ == "__main__":
    main()


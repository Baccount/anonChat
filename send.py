import socket
import socks
import requests

def send_onion_message(username):
    # Socks proxy configuration
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

    # Connect to the Onion network
    try:
        server = ("bmgwjnxnmzdyhe373grb6mv4423cublw6ot7aziovs53bcbrmrhsnhyd.onion", 80)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server)
        while True:
            # Get the message to send from the user
            message = input("Enter the message to send: ")
            # Send the message
            s.send(username.encode() + " : ".encode() + message.encode())
            # Receive the response
            response = s.recv(1024)
            print("Received response: %s" % response.decode())
    except KeyboardInterrupt:
        s.close()
    finally:
        s.close()


# Get the message to send from the user
send_onion_message("testuser")
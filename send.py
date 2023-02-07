import socket
import socks

def send_onion_message(message, onion):
    # Socks proxy configuration
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

    # Connect to the Onion network
    server = (onion, 80)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server)

    # Send the message
    s.send(message.encode())
    s.close()

# Get the message to send from the user
message = input("Enter message to send: ")
onion = input("Enter onion address: ")
send_onion_message(message, onion)
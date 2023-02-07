import socket
import socks
import requests

# change the color of the text
def color_str(username, color):
    if color == "red":
        return "\033[31m" + username + "\033[0m"
    elif color == "green":
        return "\033[32m" + username + "\033[0m"
    elif color == "yellow":
        return "\033[33m" + username + "\033[0m"
    elif color == "blue":
        return "\033[34m" + username + "\033[0m"
    else:
        return username


def send_onion_message(username, onion):
    # Socks proxy configuration
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

    # Connect to the Onion network
    try:
        server = (onion, 80)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server)
        # send the username to the server
        s.send(username.encode())
        while True:
            # Get the message to send from the user
            message = input("Enter the message to send: ")
            # Send the message
            s.send(message.encode())
            # Receive the message
            message = s.recv(4096).decode()
            # Print the message
            print(message)
    except KeyboardInterrupt:
        s.close()
    finally:
        s.close()

# Get the onion address from the user
onion = input("Enter the onion address: ")
# get thew username from the user
username = input("Enter the username: ")
# get the color of the username from the user
color = input("Enter the color of the username: ")
username = color_str(username, color)
# Get the message to send from the user
send_onion_message(username, onion)
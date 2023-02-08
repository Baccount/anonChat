import socket
import socks
import threading



shutdown_flag = False

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

def receive_message(s, username, onion):
    while True:
        try:
            # Receive the message
            receive = s.recv(4096).decode()
            # Print the message
            if receive:
                print('\r' + receive)
        except KeyboardInterrupt:
            break
        except ConnectionResetError:
            # reset the connection
            #s.close()
            send_onion_message(username, onion)
            break


def send_onion_message(username, onion):
    # Connect to the Onion network
    try:
        # Socks proxy configuration
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        server = (onion, 80)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server)
        # send the username to the server
        s.send(username.encode())
        # run seprate thread that receives messages
        thread = threading.Thread(target=receive_message, args=(s, username, onion,))
        thread.start()
        while True:
            # Get the message to send from the user
            message = input(f"(me) {username}: ")
            # Send the message
            s.send(message.encode())
    except ConnectionResetError:
        # reset the connection
        #s.close()
        print("Connection reset error")
        send_onion_message(username, onion)
    except KeyboardInterrupt:
        print("Keyboard Interrupt, shutting down")
        thread.join()
    finally:
        # close the socket
        s.close()
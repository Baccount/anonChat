# import the send and receive modules
from send import send_onion_message, color_str






# Get the onion address from the user
onion = input("Enter the onion address: ")
# get thew username from the user
username = input("Enter the username: ")
# get the color of the username from the user
color = input("Enter the color of the username: ")
username = color_str(username, color)
# Get the message to send from the user
try:
    send_onion_message(username, onion)
except KeyboardInterrupt:
    print("Exiting...")
    exit()
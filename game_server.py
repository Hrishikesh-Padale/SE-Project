import sys
import threading
from socket import *

host = '127.0.0.1'

port = 13000

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
server.bind((host, port))

server.listen(10)

#Storing client names and connections in the lists
clients = []
username = []


def get_username_and_message(message):
    username = ""
    msg = ""
    for i in message:
        if i != ":":
            username += i
    msg = message[len(username)+1:]
    return username

#Send message recieved from a user to all users
def broadcast(message):
    for client in clients:
        client.send(message)

#It recieves messages from the clients. This function is driven by the threads
#From each thread message is recieved and send to broadcast function to send it all the users
#If exception occures the function will close the client connection and removes client from client list

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user = username[index]
            message = '{} disconnected'.format(user.encode())
            broadcast(message.encode())
            break

#This primary function first recieves messages from new users
#First it will take username from the client and appent it to the username and client list
#It send hello message to the client and activates its thread    
def recieve_messages():
    while True:
        client, addr = server.accept()
        print("Connected with {}".format(str(addr)))
        user = client.recv(1024).decode()
        username.append(user)
        clients.append(client)

        print("{} connected".format(user))
        message = "Welcome to the chatroom"
        client.send(message.encode())

        thread = threading.Thread(target = handle_client, args = (client, ))
        thread.start()

print("Server is ready to recieve messages")
recieve_messages()

print("Closing server")
server.close()

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 12:49:07 2020

@author: polor
"""
import threading
import socket


from log import *
from user import *

host="127.0.0.1"
port=5001

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            index=clients.index(client)
            nickname=nicknames[index]

            message=client.recv(1024).decode("ascii")
            message = "{} : {}".format(nickname, message)
            message = message.encode("ascii")
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break
        
def receive():
    while True:
        nickname=""

        client, address=server.accept()
        print(f"Connect with " +str(address))
        
        log=-1
        while log != 0:
            messageTexte = client.recv(1024).decode('ascii').strip()

            if messageTexte[0:3]=='log':
                arg=messageTexte.split(' ')[1:3]
                log=signin(arg[0],arg[1])
                nickname = arg[0]
                if log==0:
                    client.send(f'Success log'.encode('ascii'))
                elif log==1:
                    client.send(f'Incorrect Password'.encode('ascii'))
                else:
                    signup(arg[0],arg[1])
                    client.send(f'Created an account'.encode('ascii'))
                    log = 0

        nicknames.append(nickname)
        clients.append(client)
        
        print(f'Nickname of the client is '+ nickname)
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to the server !'.encode('ascii'))
        
        thread= threading.Thread(target= handle, args=(client,))
        thread.start()
print('server is listening...')
receive()
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:07:07 2020

@author: polor
"""

import socket
import threading
from EnvoieFichierServeur import envoi_fichier
from EnvoieFichierClient import recv_file


#nickname= input("Choose a nickname\n")

print("Loggez vous avec la command 'log USERNAME PASSWORD'\n")

host="127.0.0.1"
port=5001
client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def receive():
    while True:
        try:


            message=client.recv(1024).decode('ascii')

            if message == "rcv":
                recv_file()
                continue
            print(message)
        except Exception as e:
            print(e)
            print("An error occured")
            client.close()
            break
        
        
def write():
    while True:
        message = f'{input()}'
        client.send(message.encode('ascii'))

        if message[0:3] == "snd":
            arg = message.split(' ')[1].strip()
            envoi_fichier(arg, host)
        
receive_thread= threading.Thread(target=receive)
receive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()

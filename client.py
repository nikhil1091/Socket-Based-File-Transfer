import socket
import sys
import os
from port_availibility import checkHost 
import hashlib 

connections=list()
frame_size=100
server_toggle=0
sockets=[]

def config_connections():    

    global connections

    ip1=input("Enter server 1 IP address: ")
    port1=input("Enter the port 1 number: ")
    port1=int(port1,10)
    if checkHost(ip1,port1):
        connections.append((ip1,port1))

    ip2=input("Enter server 2 IP address: ")
    port2=input("Enter the port 2 number: ")
    port2=int(port2,10)
    if checkHost(ip2,port2):
        connections.append((ip2,port2))


def create_socket():
    
    global connections,sockets
    for elem in connections:
        socket1=socket.socket()
        socket1.connect(elem.first,elem.second)
        sockets.append(socket1)

def create_frame(data,frame_number):
    data=str(frame_number)+data
    checksum=hashlib.md5(data)
    data=data+checksum
    return data



def split_data(file, frame_size):
    while True:
        data = file.read(frame_size)
        if not data:
            break
        yield data

def send(data):
    socket=config_socket()
    if socket is None:
        return False    


config_connections()
create_socket()

filename=input("Enter the path to the file: ")
frame_size=input("Enter the frame size(in KB) :")
frame_size=int(frame_size)

frame_number=0
try:
    with open(filename) as file:

        for data in split_data(file,frame_size):
            frame_number+=1
            data=create_frame(data,frame_number)
            result=send(data)
            if not result:
                print("File not sent")
                exit
            

            



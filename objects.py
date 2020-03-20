import hashlib
from constants import *
echar="+=+=+=+=/+\=+=+=+=+=+=+"
flag="*7*#E^$%^IDFEDFMKFXSE%$S$$%$*"

max_attempts=10
rttime=100
frame_size_recv=1000000
# global max_attempts,frame_size,rttime

def just_send(server_socket,message):
        # print("At send", message)
        global max_attempts,frame_size
        message=message.encode()
        try:
                server_socket.sendall(message)
                return True
        except Exception as e: 
                print(e)
                print("sending failed - justsend ",message)
        return False

def just_recieve(server_socket):
        # print("At receive")
        global max_attempts,frame_size
        try:
                # print(cls.frame_size)
                message=server_socket.recv(frame_size_recv)
                message=message.decode()
                return True,message
        except Exception as e: 
                print(e)
                print("recieve failed- just-recieve")
                return False,""
        return False,""

def send_wait_receive(server_socket,message):
                # global variables
                # print("At send wait receive", message)
                global max_attempts,frame_size
                # end
                # check if socket is live
                message=message.encode()
                try:
                        server_socket.sendall(message)
                except Exception as e: 
                        print(e)
                        return False,""

                for attempts in range(max_attempts):
                        # print("attempting at send wait receive ",attempts)
                        try:
                                reply=server_socket.recv(frame_size_recv)
                                reply=reply.decode()
                                return True,reply    
                        except Exception as e: 
                                print(e)
                                print("waited long error")
                        return False,""
                return False,""


class utility:
        
        
        max_attempts=10
        frame_size=1024

        def __init__(self,max_attempts,frame_size):
                
                self.max_attempts=max_attempts
                self.frame_size=frame_size

                return
        
        @classmethod
        def just_send(cls,server_socket,message):
                message=message.encode()
                try:
                        server_socket.sendall(message)
                        return True
                except Exception as e: 
                        print(e)
                        print("sending failed - justsend ",message)
                return False
        @classmethod
        def just_recieve(cls,server_socket):
                try:
                        # print(cls.frame_size)
                        message=server_socket.recv(cls.frame_size)
                        message=message.decode()
                        return True,message
                except Exception as e: 
                        print(e)
                        print("recieve failed- just-recieve")
                        return False,""
                return False,""

        @classmethod
        def send_wait_receive(cls,server_socket,message):
                # global variables

                # end
                # check if socket is live
                message=message.encode()
                try:
                        server_socket.sendall(message)
                except Exception as e: 
                        print(e)
                        return False

                for attempts in range(cls.max_attempts):
                        try:
                                reply=server_socket.recv(1024)
                                reply=reply.decode()
                                return True,reply    
                        except Exception as e: 
                                print(e)
                                print("waited long error")
                        return False,""

class frame_blueprint:
        def __init__(self,frame_number=-100,content=""):
                if frame_number!=-100:
                        self.header=str(frame_number)
                        self.content=str(content)

                        checksum=hashlib.md5(self.content.encode())
                        checksum=checksum.digest()
                        checksum=str(checksum)
                        self.trailer=checksum
                        # self.size=len(self.header)+len(self.content)+len(self.trailer)
                        self.size="1"
                        self.valid=True
                        return
                else:
                        data=content.split(echar)
                        self.size=int(data[0],10)
                        self.header=data[1]
                        self.content=data[2]
                        self.trailer=data[3]

                        checksum=hashlib.md5(self.content.encode())
                        checksum=checksum.digest()
                        checksum=str(checksum)
                        data_size=1
                        # data_size=len(self.header)+len(self.content)+len(self.trailer)
                        # print(checksum,self.trailer,self.size,data_size)
                        
                        if checksum==self.trailer and self.size==data_size:
                                self.valid=True
                        else:
                                self.valid=False
                        return
                

        def to_string(self):
                
                string=str(self.size)+echar+self.header+echar+self.content+echar+self.trailer
                return string
        
# if __name__=="__main__":
#         # global max_attempts,frame_size
#         frame_size=input("Enter the size of the  frame in KB : ")
#         frame_size=int(frame_size,10)
#         rttime=input("Enter the rtt : ")
#         rttime=int(rttime,10)
#         max_attempts=input("Enter the maximum number of resends : ")
#         max_attempts=int(max_attempts,10)

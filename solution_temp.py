#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
   serverSocket = socket(AF_INET, SOCK_STREAM)
   #Prepare a sever socket
   serverSocket.bind(('127.0.0.1', 13331))
   serverSocket.listen(10)

   while True:
       #Establish the connection
       connectionSocket, addr = serverSocket.accept()
       try:
           message = connectionSocket.recv(1024)
           filename = message.split()[1]

           f = open(filename[1:])
           data = f.read(1024)
           connectionSocket.send(bytes(data.encode()))
           while data != bytes(''.encode()):
               # print(data)
               data = f.read(1024)
               connectionSocket.send(bytes(data.encode()))
           connectionSocket.close()

       except IOError:
           #Send response message for file not found (404)
           response = '404 Not Found \r\n'
           connectionSocket.send(response.encode())
           connectionSocket.close()

   serverSocket.close()
   sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
   webServer(13331)
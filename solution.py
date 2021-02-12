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
           outputdata = f.read()
           f.close()

           #Send one HTTP header line into socket
           response = 'HTTP/1.0 200 OK\n\n'
           connectionSocket.sendall(response.encode())

           #Send the content of the requested file to the client
           for i in range(0, len(outputdata)):
                response = outputdata[i]
                connectionSocket.send(response.encode())
           connectionSocket.close()

       except IOError:
           #Send response message for file not found (404)
           response = '404 Not Found \r\n'
           connectionSocket.send(response.encode())
           connectionSocket.close()
       except BrokenPipeError:
           connectionSocket.close()


   serverSocket.close()
   sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
   webServer(13331)
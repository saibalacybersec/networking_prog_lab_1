from socket import *
import sys # In order to terminate the program


#python -m smtpd -c DebuggingServer -n 127.0.0.1:1025
def smtp_client(port='1025', mailserver='127.0.0.1'):
   # try:
         mailserver = (mailserver, port)
         msg = "\r\n My message"
         endmsg = "\r\n.\r\n"

         clientSocket = socket(AF_INET, SOCK_STREAM)
         clientSocket.connect(("127.0.0.1",1025))

         recv = clientSocket.recv(1024).decode()
         # print("#0 RECV : Response from connection :" + recv)

         if recv[:3] != '220':
             # print('220 reply not received from server.')
             quit

         # Send HELO command and print server response.
         heloCommand = 'HELO Alice\r\n'
         clientSocket.send(heloCommand.encode())
         recv1 = clientSocket.recv(1024).decode()
         # print(recv1)
         if recv1[:3] != '250':
               print('250 reply not received from server.')
               quit
         clientSocket.close()
   # except:
   #       clientSocket.close()

if __name__ == '__main__':
   # smtp_client(25, 'smtp.nyu.edu')
   smtp_client(1025, '127.0.0.1')
   # smtp_client(1025, 'smtp.gmail.com')
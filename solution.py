from socket import *
import sys # In order to terminate the program


#python -m smtpd -c DebuggingServer -n 127.0.0.1:1025
def smtp_client(port='1025', mailserver='127.0.0.1'):
   try:
         mailserver = (mailserver, port)
         msg = "\r\n My message"
         endmsg = "\r\n.\r\n"
         # Create socket called clientSocket and establish a TCP connection with mailserver and port
         # print("Starting...." + str(mailserver))

         clientSocket = socket(AF_INET, SOCK_STREAM)
         clientSocket.connect(mailserver)

         recv = clientSocket.recv(1024).decode()
         # print("#0 RECV : Response from connection :" + recv)
         if recv[:3] != '220':
             # print('220 reply not received from server.')
             quit

         # Send HELO command and print server response.
         helloCommand = 'HELO localhost\r\n'
         clientSocket.send(helloCommand.encode())
         recv1 = clientSocket.recv(1024).decode()
         # print(" #1 RECV : " + recv1)
         if recv1[:3] != '250':
             # print('250 reply not received from server.')
             quit

         # Send MAIL FROM command and print server response.
         mailFrom = "MAIL FROM:<sl8062@nyu.edu>\r\n"
         clientSocket.send(mailFrom.encode())
         recv2 = clientSocket.recv(1024)
         recv2 = recv2.decode()
         # print("#2 RECV2 : " + recv2)

         # Send RCPT TO command and print server response.
         sendTo = 'RCPT TO:<sl8062@nyu.edu>\r\n'
         clientSocket.send(sendTo.encode())
         recv3 = clientSocket.recv(1024)
         recv3 = recv3.decode()
         # print("After send TO" + recv3)

         # Send DATA command and print server response.
         data = 'DATA\r\n'
         clientSocket.send(data.encode())
         recv4 = clientSocket.recv(1024)
         recv4 = recv4.decode()
         # print("After DATA command: " + recv4)

         # # Send message data.
         clientSocket.send(msg.encode())
         # Message ends with a single period.
         clientSocket.send(endmsg.encode())
         recv6 = clientSocket.recv(1024)
         recv6 = recv6.decode()
         # print("Step 6 RECV6" + recv6)

         # Send QUIT command and get server response.
         quit = "QUIT\r\n"
         clientSocket.send(quit.encode())
         recv_7 = clientSocket.recv(1024)
         # print(" Last Step# RECV 7 :" + recv_7.decode())
         clientSocket.close()
   except:
         clientSocket.close()

if __name__ == '__main__':
   smtp_client(25, 'smtp.nyu.edu')
   # smtp_client(1025, '127.0.0.1')

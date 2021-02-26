from socket import *
import sys # In order to terminate the program


#python -m smtpd -c DebuggingServer -n 127.0.0.1:1025
def smtp_client(port='1025', mailserver='127.0.0.1'):

   mailserver = (mailserver, port)

   # Create socket called clientSocket and establish a TCP connection with mailserver and port
   # print("Starting...." + str(mailserver))
   clientSocket = socket(AF_INET, SOCK_STREAM)
   clientSocket.connect(mailserver)

   recv = clientSocket.recv(1024).decode()
   # print(" Response from connection :" + recv)
   if recv[:3] != '220':
       print('220 reply not received from server.')
       exit()
   # Send HELO command and print server response.
   heloCommand = 'HELO Alice\r\n'
   clientSocket.send(heloCommand.encode())
   recv1 = clientSocket.recv(1024).decode()
   # print("recv1: " + recv1)
   if recv1[:3] != '250':
       print('250 reply not received from server.')
       exit()
   # Send MAIL FROM command and print server response.
   mailFrom = "MAIL FROM: <saibalasrini@mail.com>\r\n"
   clientSocket.send(mailFrom.encode())
   recv2 = clientSocket.recv(1024)
   recv2 = recv2.decode()
   # print("After MAIL FROM Cmd" + recv2)

   # Send RCPT TO command and print server response.
   sendTo = 'RCPT TO: <saibalasrini@gmail.com>\r\n'
   clientSocket.send(sendTo.encode())
   recv3 = clientSocket.recv(1024)
   recv3 = recv3.decode()
   # print("After send TO" + recv3)

   # Send DATA command and print server response.
   data = 'DATA\r\n test'
   clientSocket.send(data.encode())
   recv4 = clientSocket.recv(1024)
   recv4 = recv4.decode()
   # print("After DATA command: " + recv4)

   # msg = '\r\n My message'
   # # Send message data.
   # clientSocket.send(msg.encode())
   # print("Message sent")
   # recv_5 = clientSocket.recv(1024)
   # print("Response after sending message data:" + recv_5.decode())

   endmsg = "\r\n.\r\n"
   # Message ends with a single period.
   clientSocket.send(endmsg.encode())
   recv_6 = clientSocket.recv(1024)
   # print("Response after sending message with single period:" + recv_6.decode())

   # Send QUIT command and get server response.
   quit = "QUIT\r\n"
   clientSocket.send(quit.encode())
   recv_7 = clientSocket.recv(1024)
   # print(recv_7.decode())
   clientSocket.close()


if __name__ == '__main__':
   smtp_client(1025, '127.0.0.1')


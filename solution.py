from socket import *
import os
import sys
import struct
import time
import select
import binascii
import statistics
# Should use stdev

ICMP_ECHO_REQUEST = 8

rtt_array = []
packet_min = 0
packet_avg = 0
packet_max = 0
stdev_var = 0

#starting
# test 2

def checksum(string):
   csum = 0
   countTo = (len(string) // 2) * 2
   count = 0

   while count < countTo:
       thisVal = (string[count + 1]) * 256 + (string[count])
       csum += thisVal
       csum &= 0xffffffff
       count += 2

   if countTo < len(string):
       csum += (string[len(string) - 1])
       csum &= 0xffffffff

   csum = (csum >> 16) + (csum & 0xffff)
   csum = csum + (csum >> 16)
   answer = ~csum
   answer = answer & 0xffff
   answer = answer >> 8 | (answer << 8 & 0xff00)
   return answer



def receiveOnePing(mySocket, ID, timeout, destAddr):
   timeLeft = timeout
   rtt_cnt = 0
   rtt_sum = 0

   while 1:
       startedSelect = time.time()
       whatReady = select.select([mySocket], [], [], timeLeft)
       howLongInSelect = (time.time() - startedSelect)
       #print("whatReady[0]=" + str(whatReady[0]) + " whatReady[1]= " + str(whatReady[1]) )
       if whatReady[0] == []:  # Timeout
           return "Request timed out."

       timeReceived = time.time()
       recPacket, addr = mySocket.recvfrom(1024)
       # print("recPacket" + str(recPacket))
       # Fill in start

       # Fetch the ICMP header from the IP packet
       icmpheader = recPacket[20:28]
       struct_format = "bbHHh"
       unpacked_data = struct.unpack(struct_format, icmpheader)
       # print(unpacked_data)
       type, code, check_sum, packetid, seq = struct.unpack(struct_format, icmpheader)
       # print(type, code, check_sum, packetid, "icmp_seq =", seq)
       packet = struct.unpack('d', recPacket[28:])
       ip_header = struct.unpack('!BBHHHBBH4s4s', recPacket[:20])
       length = len(recPacket) - 20
       ttl = ip_header[5]
       rtt = (timeReceived - packet[0])
       rtt_cnt += 1
       rtt_sum += rtt
       # rtt_array[rtt_cnt] = rtt
       # print(" rtt_array " + str(rtt_cnt) )
       return 'Reply from {}: bytes={} time={:.7f} ms ttl={} '.format(destAddr, length, rtt,ttl)
       # Fill in end

       timeLeft = timeLeft - howLongInSelect
       if timeLeft <= 0:
           return "time left  Request timed out."


def sendOnePing(mySocket, destAddr, ID):
   # Header is type (8), code (8), checksum (16), id (16), sequence (16)

   myChecksum = 0
   # Make a dummy header with a 0 checksum
   # struct -- Interpret strings as packed binary data
   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   data = struct.pack("d", time.time())
   # Calculate the checksum on the data and the dummy header.
   myChecksum = checksum(header + data)


   # Get the right checksum, and put in the header

   if sys.platform == 'darwin':
       # Convert 16-bit integers from host to network  byte order
       myChecksum = htons(myChecksum) & 0xffff
   else:
       myChecksum = htons(myChecksum)


   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   packet = header + data

   mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str


   # Both LISTS and TUPLES consist of a number of objects
   # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
   icmp = getprotobyname("icmp")


   # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
   mySocket = socket(AF_INET, SOCK_RAW, icmp)

   myID = os.getpid() & 0xFFFF  # Return the current process i
   sendOnePing(mySocket, destAddr, myID)
   delay = receiveOnePing(mySocket, myID, timeout, destAddr)
   mySocket.close()
   return delay


def ping(host, timeout=1):
   # timeout=1 means: If one second goes by without a reply from the server,      # the client assumes that either the client's ping or the server's pong is lost
   dest = gethostbyname(host)
   # print("Pinging " + dest + " using Python:")
   # print("")

   packet_array = list()
   # packet_min = 0.000000
   # packet_max =0.000000
   packet_sum = 0.000000
   stdev_var = 0.000000
   # Send ping requests to a server separated by approximately one second
   for i in range(0,4):
       delay = doOnePing(dest, timeout)
       # print("delay" + str(delay.ttl))
       print(delay)
       if delay!="Request timed out":
           start = delay.find('time') + 5
           end = delay.find(' ms', start)
           packet_array.append(float(delay[start:end]))
           # packet_min = min(packet_min, float(delay[start:end]))
           # packet_max = max(packet_max, float(delay[start:end]))
           packet_sum += float(delay[start:end])
       time.sleep(1)  # one second
   # Calculate vars values and return them
   packet_min = min(packet_array)
   packet_max = max(packet_array)
   packet_avg = (packet_sum/len(packet_array))
   stdev_var = statistics.stdev(packet_array,None)

   vars = [round(packet_min, 2), round(packet_avg, 2), round(packet_max, 2),round(stdev_var, 2)]
   # print (" vars " + str(vars))
   # print("packet_min " + str(packet_min) + "packet_max " + str(packet_max) + "packet_sum" + str(packet_sum)+ " packet_avg" + str(packet_avg) + " stddev " + str(stdev_var))
   return vars

if __name__ == '__main__':
   ping("google.co.il")
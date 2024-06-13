import socket
import struct
import binascii

# IP address of given machine
HOST = socket.gethostbyname(socket.gethostname())

# create a raw socket and bind it to the machine IP address
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

# Include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# receive all packets
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# disabled promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


while True:
    print(1)
    packet = s.recvfrom(2048)
    eth_header = packet[0][0:14]
    header = struct.unpack("!6s6s2s", eth_header)
    print("Destination MAC:" + binascii.hexlify(header[0]) + 
          " Source MAC:" + binascii.hexlify(header[1]) + " Type:" + binascii.hexlify(header[2]))
    
    ipheader = packet[0][14:34]
    ipheader_unpack = struct.unpack("!12s4s4s", ipheader)
    print("Source IP:" + socket.inet_ntoa(ipheader_unpack[1]) + 
          " Destination IP:" + socket.inet_ntoa(ipheader_unpack[2]))

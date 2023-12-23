import socket
import constants
import packet
import datetime


"""
data = "RUCHAN ABİ NABAN cura abi azd azd azd azd azd azd"
seq = 1231233121
stream_id = 1
sent_time = datetime.datetime.now().timestamp()
paket = packet.packet(seq,stream_id,data.encode())
paket.sent_time = sent_time
willsend = paket.pack()
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ip = '192.168.1.7'
port = 65432
sock.sendto(willsend,(ip,port))
"""
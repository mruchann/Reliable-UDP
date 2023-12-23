import socket
import packet
import constants


"""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('',65432))
message, address = sock.recvfrom(constants.PACKET_TOTAL_SIZE)
sequence_number, payload, stream_id = packet.unpack(message)
print(f"payload : {payload.decode()} sequence_number: {sequence_number}")
"""

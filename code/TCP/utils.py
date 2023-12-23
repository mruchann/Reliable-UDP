# import socket
# import struct
# import fcntl
#
#
# def get_ip_address(sock, interface_name='eth0'):
#     return socket.inet_ntoa(fcntl.ioctl(
#         sock.fileno(),
#         0x8915,  # SIOCGIFADDR
#         struct.pack('256s', interface_name)
#     ))
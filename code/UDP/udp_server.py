import socket
from collections import deque

import utils
import constants
from packet import *
import datetime

# data = "RUCHAN ABİ NABAN cura abi azd azd azd azd azd azd"
# seq = 1231233121
# stream_id = 1
# sent_time = datetime.datetime.now().timestamp()
# paket = packet(seq,stream_id,data.encode())
# paket.sent_time = sent_time
# willsend = paket.pack()
# sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# ip = '172.17.0.3'
# port = 65432
# sock.sendto(willsend,(ip,port))


class udp_server:
    def __init__(self, serverHost, serverPort, clientHost, clientPort, data=None):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.clientHost = clientHost
        self.clientPort = clientPort
        self.data = data

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind((self.serverHost, self.serverPort))

        self.serverSocket.setblocking(False)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8388608)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8388608)

        self.sequence_number = 1
        self.stream_id = 0
        self.duplicate_ack_count = 0

        self.server_window = deque()
        self.fill_window()

    def fill_window(self):
        while len(self.server_window) < constants.WINDOW_SIZE:
            try:
                chunk = next(self.data)

                self.server_window.append(packet(self.sequence_number, self.stream_id, chunk, constants.WAITING))
                self.sequence_number += 1

                if len(chunk) == 0:
                    self.stream_id += 1

            except StopIteration:
                break

    def send_to_client(self):
        while self.server_window:
            packet_to_send = self.server_window[0]
            packet_to_send.sent_time = utils.get_current_timestamp()
            packet.state = constants.SENT

            self.serverSocket.sendto(packet_to_send.pack(), (self.clientHost, self.clientPort))

            print(f"we sent seq:{packet_to_send.sequence_number}")

            try:
                ack_packet, _ = self.serverSocket.recvfrom(constants.ACK_PACKET_SIZE)
                ack_seq = unpack_ack(ack_packet)

                if ack_seq <= self.server_window[0].sequence_number:
                    self.duplicate_ack_count += 1
                    if self.duplicate_ack_count == 3:
                        self.duplicate_ack_count = 0
                        continue

                self.duplicate_ack_count = 0

                while self.server_window and self.server_window[0].sequence_number < ack_seq:
                    self.server_window.popleft()

                for p in self.server_window:
                    cur_time = utils.get_current_timestamp()
                    if cur_time - p.sent_time > constants.PACKET_TIMEOUT_IN_SECONDS:
                        p.sent_time = cur_time
                        self.serverSocket.sendto(p.pack(), (self.clientHost, self.clientPort))

                self.fill_window()

            except BlockingIOError:
                pass

    def close_socket(self):
        self.serverSocket.close()
import socket
from packet import *
import constants
from collections import deque

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind(('',65432))
# message, address = sock.recvfrom(constants.PACKET_TOTAL_SIZE)
# sequence_number, payload, stream_id = unpack(message)
# print(f" payload : {payload.decode()} sequence_number: {sequence_number}")


class udp_client:
    def __init__(self, clientHost, clientPort):
        self.clientHost = clientHost
        self.clientPort = clientPort

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.bind((self.clientHost, self.clientPort))

        self.clientSocket.setblocking(False)
        self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8388608)
        self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8388608)

        self.sequence_number = 1

        self.finished_files = 2 * constants.NUMBER_OF_FILES * [False] # 0...19
        self.client_window = deque()

        self.fill_window_with_ack()


    def fill_window_with_ack(self):
        while len(self.client_window) < constants.WINDOW_SIZE:
            try:
                self.client_window.append(packet(self.sequence_number))
                self.sequence_number += 1

            except StopIteration:
                break

    def transmission_not_ended(self):
        for stream_id in range(2 * constants.NUMBER_OF_FILES): # 0...19
            if not self.finished_files[stream_id]:
                return True
        return False

    def receive_from_server(self):
        while self.transmission_not_ended():
            try:
                data, server_address = self.clientSocket.recvfrom(constants.PACKET_TOTAL_SIZE)
                sequence_number, payload, stream_id = unpack(data)
                self.client_window.popleft()
                self.fill_window_with_ack()

                print("we get: ",sequence_number, stream_id)

                if data is not None and sequence_number <= self.client_window[-1].sequence_number: # goray abi d
                    for p in self.client_window:
                        if p.sequence_number == sequence_number:
                            p.payload = payload
                            p.state = constants.RECEIVED
                            p.stream_id = stream_id

                    if len(data) == 0:
                        self.finished_files[stream_id] = True
                        self.client_window.popleft()

                    while self.client_window:
                        if self.client_window[0].state != constants.RECEIVED:
                            break
                        if self.client_window[0].stream_id is not None and self.finished_files[self.client_window[0].stream_id]:
                            self.client_window.popleft()


                    while self.client_window and self.client_window[0].state == constants.RECEIVED:
                        if len(data) == 0:
                            self.finished_files[stream_id] = True
                            self.client_window.popleft()
                            continue

                        yield self.client_window[0].payload, self.client_window[0].stream_id

                        ack_packet = packet(self.client_window[0].sequence_number)

                        self.clientSocket.sendto(ack_packet.pack_ack(), server_address)

                        self.client_window.popleft()
                        self.fill_window_with_ack()

                else: # arrived packet is corrupted
                    self.clientSocket.sendto(packet(sequence_number).pack_ack(), server_address)

            except BlockingIOError:
                pass

    # close the socket connection
    def close_socket(self):
        self.clientSocket.close()
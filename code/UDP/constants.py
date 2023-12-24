# packet states
WAITING = 0
SENT = 1
RECEIVED = 2

# we've just used brute force method for finding the variable sizes

#packet
PACKET_HEADER_SIZE = 36 # sequence number(4) + stream_id(2) + sent_time(8) + state(2) + payload_size(4) + checksum(16)
PACKET_PAYLOAD_SIZE = 1325
PACKET_TOTAL_SIZE = PACKET_HEADER_SIZE + PACKET_PAYLOAD_SIZE

ACK_PACKET_SIZE = 20 # sequence number(4) + checksum(16)

PACKET_TIMEOUT_IN_SECONDS = 1

# 10 large and 10 small files
NUMBER_OF_FILES = 10

# port numbers
UDP_CLIENT_PORT = 50000
UDP_SERVER_PORT = 60000

# Size of the receiver (client) and sender (server) windows
WINDOW_SIZE = 1120 #1150
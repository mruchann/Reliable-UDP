import constants
import struct
import utils


class packet:
    # update header/payload size if there is a change here
    def __init__(self, sequence_number, stream_id=None, payload=None, state=constants.WAITING):
        self.sequence_number = sequence_number  # I -> 4 bytes
        self.stream_id = stream_id  # H -> 2 bytes
        self.sent_time = None  # d -> 8 bytes
        self.state = state  # H -> 2 bytes
        self.payload = payload  # Variable length
        self.payload_size = None  # I -> 4 bytes
        self.checksum = None  # s -> 16 bytes

    def pack(self):
        self.payload_size = len(self.payload)
        self.checksum = self.calculate_checksum()
        free_space = constants.PACKET_PAYLOAD_SIZE - self.payload_size
        return struct.pack(f'!I16sHdHI{self.payload_size}s{free_space}s', self.sequence_number, self.checksum,
                           self.stream_id, self.sent_time, self.state, self.payload_size, self.payload,
                           b'' * free_space)

    def pack_ack(self):
        checksum = utils.calculate_checksum(bytes(str(self.sequence_number), 'utf8'))
        return struct.pack(f'!I16s', self.sequence_number, checksum)

    def calculate_checksum(self):
        data = self.payload + bytes(str(self.sequence_number), 'utf8') + bytes(str(self.stream_id), 'utf8') + \
               bytes(str(self.state), 'utf8')

        return utils.calculate_checksum(data)

    def calculate_checksum_ack(self):
        data = bytes(str(self.sequence_number), 'utf8')
        return utils.calculate_checksum(data)


def unpack(received_packet):
    sequence_number, checksum, stream_id, sent_time, state, payload_size = struct.unpack(f'!I16sHdHI', received_packet[
                                                                                                       :constants.PACKET_HEADER_SIZE])
    free_space = constants.PACKET_PAYLOAD_SIZE - payload_size
    payload, _ = struct.unpack(f'{payload_size}s{free_space}s',
                               received_packet[constants.PACKET_HEADER_SIZE:constants.PACKET_TOTAL_SIZE])

    if checksum == utils.calculate_checksum(
            payload + bytes(str(sequence_number), 'utf8') + bytes(str(stream_id), 'utf8') + \
            bytes(str(state), 'utf8')):
        return sequence_number, payload, stream_id

    return None, None, None


def unpack_ack(received_packet):
    seq, checksum = struct.unpack(f'!I16s', received_packet)
    if checksum == utils.calculate_checksum(bytes(str(seq), 'utf8')):
        return seq
    return None

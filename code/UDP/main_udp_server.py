from udp_server import *
import constants


def payload_yielder(chunk_size=constants.PACKET_PAYLOAD_SIZE):
    for i in range(10):
        with open("../../root/objects/large-" + str(i) + ".obj", "rb") as f:
            while True:
                chunk = f.read(constants.PACKET_TOTAL_SIZE)
                if not chunk:
                    break
                yield chunk
        yield b''  # indicates the end of a file

        with open("../../root/objects/small-" + str(i) + ".obj", "rb") as f:
            while True:
                chunk = f.read(constants.PACKET_PAYLOAD_SIZE)
                if not chunk:
                    break
                yield chunk
        yield b''


if __name__ == '__main__':
    udp_server = udp_server("172.17.0.2", constants.UDP_SERVER_PORT,
                            "172.17.0.3", constants.UDP_CLIENT_PORT,
                            payload_yielder())
    udp_server.send_to_client()
    udp_server.close_socket()

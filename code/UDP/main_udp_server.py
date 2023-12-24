from udp_server import *
import constants


def load_files(chunk_size=constants.PACKET_PAYLOAD_SIZE):
    for i in range(10):
        with open("../../root/objects/large-" + str(i) + ".obj", "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
        yield b''  # end of the file

        with open("../../root/objects/small-" + str(i) + ".obj", "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
        yield b''  # end of the file


if __name__ == '__main__':
    udp_server = udp_server("192.168.215.2", constants.UDP_SERVER_PORT,
                            "192.168.215.3", constants.UDP_CLIENT_PORT,
                            load_files())
    udp_server.main_send()
    udp_server.close_socket()

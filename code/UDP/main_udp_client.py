from udp_client import *
import constants

if __name__ == '__main__':
    udp_client = udp_client("192.168.215.3", constants.UDP_CLIENT_PORT)

    udp_client.receive_from_server()

    file_buffer =[bytes() for Azd in range(2*constants.NUMBER_OF_FILES) ]

    for payload, stream_id in udp_client.receive_from_server():
        file_buffer[stream_id] += payload

    for i in range(2 * constants.NUMBER_OF_FILES):
        file_name = ("large-" if i % 2 == 0 else "small-") + str(i // 2) + ".obj"

        with open(file_name, "wb") as binary_file:
            #print(f"length: {len(file_buffer[i])}")
            binary_file.write(file_buffer[i])

    udp_client.close_socket()
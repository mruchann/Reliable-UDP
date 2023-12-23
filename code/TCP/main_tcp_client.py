from tcp_client import *
import constants

if __name__ == '__main__':
    tcp_client = tcp_client(server_host='172.17.0.2', server_port=constants.TCP_PORT)

    for i in range(constants.NUMBER_OF_FILES):
        tcp_client.receive(i)

    tcp_client.close()  # Since we didn't create our socket using with block, we should close the connection explicitly.

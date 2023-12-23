from tcp_server import *
import constants

# Here is our main function for our TCP server, to operate server operations such as reading objects and sending them to the TCP client.

if __name__ == '__main__':

    # We instantiate our tcp_server with the server_host and server_port parameters.
    tcp_server = tcp_server(server_host='172.17.0.2', server_port=constants.TCP_PORT)

    # for each file index, we read a large and small file and send them by the tcp_server to the tcp_client
    for i in range(constants.NUMBER_OF_FILES):
        with open("../../root/objects/large-" + str(i) + ".obj", "rb") as binary_file:
            tcp_server.send(binary_file.read())
        with open("../../root/objects/small-" + str(i) + ".obj", "rb") as binary_file:
            tcp_server.send(binary_file.read())

    tcp_server.close()  # Since we didn't create our socket in tcp_server.py using with block, we should close the connection explicitly.

import socket
import constants

class tcp_server:
    def __init__(self, server_host, server_port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = server_host
        self.server_port = server_port

        self.serverSocket.bind((self.server_host, self.server_port))
        self.serverSocket.listen(constants.MAX_NUMBER_OF_CONNECTION)
        self.connectionSocket, _ = self.serverSocket.accept()

    def send(self, binary_file):
        self.connectionSocket.send('{:8d}'.format(len(binary_file)).encode()) # 1 byte is enough
        self.connectionSocket.sendall(binary_file)

    def close(self):
        self.connectionSocket.close()
        self.serverSocket.close()
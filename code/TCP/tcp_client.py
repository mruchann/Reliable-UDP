import socket
import constants


class tcp_client:
    def __init__(self, server_host, server_port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = server_host
        self.server_port = server_port

        self.clientSocket.connect((self.server_host, self.server_port))

    def receive(self, file_index):
        #large
        large_file_size = int(self.clientSocket.recv(constants.FILE_SIZE_LENGTH))

        large_buffer = b''

        while len(large_buffer) < large_file_size:
            # 1024 is needed because it reads a portion of a different file
            large_buffer += self.clientSocket.recv(min(large_file_size - len(large_buffer), 1024))

        large_file_name = "large-" + str(file_index) + ".obj"
        with open(large_file_name, "wb") as f:
            f.write(large_buffer)

        # small
        small_file_size = int(self.clientSocket.recv(constants.FILE_SIZE_LENGTH))

        small_buffer = b''

        # size is small, 1024 is not needed, just to make it slower

        while len(large_buffer) < large_file_size:
            small_buffer += self.clientSocket.recv(min(small_file_size - len(small_buffer), 1024))

        small_file_name = "small-" + str(file_index) + ".obj"
        with open(small_file_name, "wb") as f:
            f.write(small_buffer)

    def close(self):
        self.clientSocket.close()

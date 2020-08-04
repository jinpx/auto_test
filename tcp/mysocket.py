import socket
import time


class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.s = sock

    def connect(self, host, port):
        self.s.connect((host, port))

    def close(self):
        self.s.close()

    def send(self, msg):
        total_sent = 0
        while total_sent < len(msg):
            sent = self.s.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent
        return total_sent

    def recv(self):
        chunk = self.s.recv(2048)
        return chunk



if __name__ == '__main__':
    _my = MySocket()
    _my.connect("47.89.41.240", 37025)
    time.sleep(12)
    _my.close()
    print("Close")

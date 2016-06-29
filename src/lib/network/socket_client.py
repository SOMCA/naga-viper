import threading

from socket import socket, AF_INET, SOCK_STREAM


class SocketClient(object):

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((str(host) ,int(port)))
        print("Connection established with %s:%s" % (str(host) ,int(port)))

    def send(self, message):
	threading.Thread(target=self.socket.send, args=(message.encode('ASCII'),)).start()

    def disconnect(self):
        self.socket.close()

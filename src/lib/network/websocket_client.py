import threading

from websocket import create_connection


class WebSocketClient(object):

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def connect(self):
        self._websocket = create_connection("ws://%s:%s" % (self._host, str(self._port)))
        print("Connection as been established with %s:%s" % (self._host, str(self._port)))

    def send_data(self, data):
        # Start sending data in a new thread
        threading.Thread(target=self._websocket.send, args=(data,)).start()

    def disconnect(self):
        print("Closing websocket...")
        self._websocket.close()

from socket import socket, AF_INET, SOCK_STREAM

class SocketClient(object):

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((str(host) ,int(port)))
        print("Connection established with %s:%s" % (str(host) ,int(port)))

    def send(self, message):
        threading.Thread(target=self.socket.sendall, args=(str(message).encode('ASCII'),)).start()

    def disconnect(self):
        self.socket.close()

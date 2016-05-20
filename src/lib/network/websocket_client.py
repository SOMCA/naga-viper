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
        # Start sending data in a single thread
        threading.Thread(target=self._websocket.send, args=(data,)).start()

    def disconnect(self):
        print("Closing websocket...")
        self._websocket.close()

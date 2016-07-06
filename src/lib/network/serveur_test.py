from websocket_client import *

if __name__=='__main__':
    serveur = SocketClient()
    serveur.socket.bind(('127.0.0.1',33333))
    serveur.socket.listen(5)
    client, address = serveur.socket.accept()
    print('{} connected'.format( address ))
    while True:
        
        response = client.recv(4096)
        if response != "":
                print(response)

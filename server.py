
import socket
import threading

class TCPServer(object):
    def __init__(self, **kwargs):
        self.ip = kwargs.get('ip')
        self.port = kwargs.get('port')
        self.handle_client = kwargs.get('handle_client')

        assert(self.ip)
        assert(self.port)
        assert(self.handle_client)

        self.max_recv = kwargs.get(
            'max_recv') if kwargs.get('max_recv') else 1024
        self.client_map = {}

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen()
            while True:
                c, addr = s.accept()
                print(addr, 'connected.')
                c.sendall(b'my is server')
                t = threading.Thread(
                    target=self.my_handle_client, args=(c, addr))
                self.client_map[addr] = {
                    'addr': addr,
                    'thread': t,
                    'socket': c
                }
                t.start()

    def my_handle_client(self, c, addr):
        while True:
            data = c.recv(self.max_recv)
            if not data:
                break
            self.handle_client(self.get_client(addr), data)

    def get_client(self, addr):
        return self.client_map.get(addr)


def handle_client(client, data):
    print(data)
    socket = client.get('socket')
    socket.sendall(b'wo kwon')


if __name__ == '__main__':
    kwargs = {
        'ip': '127.0.0.1',
        'port': 1234,
        'handle_client': handle_client
    }
    server = TCPServer(**kwargs)
    server.start()

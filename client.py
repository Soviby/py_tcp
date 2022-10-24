import socket
import threading


class TCPClient(object):
    def __init__(self, ** kwargs):
        self.ip = kwargs.get('ip')
        self.port = kwargs.get('port')
        self.handle_server = kwargs.get('handle_server')

        assert(self.ip)
        assert(self.port)
        assert(self.handle_server)

        self.max_recv = kwargs.get(
            'max_recv') if kwargs.get('max_recv') else 1024

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            s.sendall(b'my is client')
            while True:
                data = s.recv(self.max_recv)
                if not data:
                    break
                self.handle_server(data)

if __name__ == '__main__':
    kwargs = {
        'ip': '127.0.0.1',
        'port': 1234,
        'handle_server': lambda data: print(data)
    }
    server = TCPClient(**kwargs)
    server.start()

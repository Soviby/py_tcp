
import socket
import threading


class TCPClinet(object):
    def __init__(self, **kwargs):
        self.addr = kwargs.get('addr')
        self.socket = kwargs.get('socket')
        self.handle_client = kwargs.get('handle_client')

        self.is_alive = True
        self.thread = threading.Thread(
            target=self.handle_client, kwargs={'client': self})

    def start(self):
        self.thread.start()

    def close(self):
        self.is_alive = False
        self.socket.close()


class TCPServer(object):
    def __init__(self, **kwargs):
        self.addr = kwargs.get('addr')
        self.handle_client = kwargs.get('handle_client')

        assert(self.addr)
        assert(self.handle_client)

        self.max_recv = kwargs.get(
            'max_recv') if kwargs.get('max_recv') else 1024
        self.client_map = {}

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.addr)
            s.listen()
            while True:
                c, addr = s.accept()
                print(addr, 'connected.')
                client = TCPClinet(addr=addr, socket=c,
                                   handle_client=self.my_handle_client)
                client.start()
                self.client_map[addr] = client

    def my_handle_client(self, client: TCPClinet):
        socket = client.socket
        while True:
            if not client.is_alive:
                break
            data = socket.recv(self.max_recv)
            if not data:
                break
            self.handle_client(client, self, data)

    def get_client(self, addr) -> TCPClinet:
        return self.client_map.get(addr)

    def remove_client(self, addr):
        client = self.get_client(addr)
        if client:
            client.close()
            del client


def handle_client(client: TCPClinet, server: TCPServer, data):
    print(data)
    client.socket.sendall(b'wo kwon')
    server.remove_client(client.addr)


if __name__ == '__main__':
    server = TCPServer(addr=('127.0.0.1', 1234), handle_client=handle_client)
    server.start()

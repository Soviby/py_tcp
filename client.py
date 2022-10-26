import sys
sys.path.append("../lib/soviby")

import socket
from helper import CommandLineParser

cmdParser = CommandLineParser()
cient = None


class TCPClient(object):
    def __init__(self, ** kwargs):
        self.addr = kwargs.get('addr')
        self.handle_server = kwargs.get('handle_server')
        assert(self.addr)
        assert(self.handle_server)

    def send(self, data):
        self.socket.sendall(data)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            self.socket = s
            while True:
                cmdParser.set_input_line()
                data = s.recv(1024)
                if not data:
                    break
                self.handle_server(data)


def handle_server(data):
    print(data)


def send(data: str):
    cient.send(bytes(data))


def start_client(args):
    global cient
    cient = TCPClient(addr=(args[1], int(args[2])),
                      handle_server=handle_server)
    cient.start()


if __name__ == '__main__':
    cmdParser.add_desc('start', kind='list[str]', func=start_client)
    cmdParser.add_desc('send', alias='s', kind='str', func=send)
    cmdParser.handle_sys_argv_command(cmdParser)

import socket
from time import strftime


class Server(object):
    def __init__(self):
        self.socket = socket.socket()
        self.ip = '127.0.0.1'
        self.listen_port = 11111
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.listen_port))

    def runs(self):
        self.socket.listen(5)
        try:
            while True:
                print('inside while')
                client_socket, client_addr = self.socket.accept()
                print('Accepted connection with {}'.format(client_addr))
                client_socket.send(b'Hello from server')
                command = client_socket.recv(15)
                self.dispatch_commands(command, client_socket)
                client_socket.close()
                break
        except socket.error as err:
            print('Binding error on port {}. Error: {}'.format(self.listen_port, err.args[1]))

    def dispatch_commands(self, command, client_socket):
        while command != b'%Hastalavista':
            if command == b'%Close':
                break
            elif command == b'%Time':
                client_socket.send(strftime('%H:%M:%S').encode())
            elif command == b'%Showtime':
                client_socket.send(b'Wait for the picture')
                file = open('Terminator2.jpg', 'rb')
                data = file.read()
                file.close()
                client_socket.send(data)
            elif command == b'%Ping':
                client_socket.send(b'pong')
            elif command == b'%Date':
                client_socket.send(strftime('%d/%b/%Y').encode())
            elif command[-1:] == b'?':
                client_socket.send(b'42')
            else:
                client_socket.send(b'Can elaborate on that?')
            command = client_socket.recv(15)


def main():
    server = Server()
    server.runs()

if __name__ == '__main__':
    main()

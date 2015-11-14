import socket


class Client(object):
    def __init__(self):
        self.socket = socket.socket()
        self.ip = '127.0.0.1'
        self.port = 11111

    def runs(self):
        try:
            self.socket.connect((self.ip, self.port))
            print(self.socket.recv(1024).decode())
            self.send_command()
        except socket.error as err:
            print('Error: {}'.format(err.args[1]))
        return

    def send_command(self):
        while True:
            command = input()
            self.socket.send(command.encode())
            if command == '%Close':
                self.socket.close()
                return
            else:
                response = self.socket.recv(240).decode()
                self.dispatch_response(response)

    def dispatch_response(self, response):
        if response == 'Wait for the picture':
            data = self.socket.recv(21504)
            file = open('ReceivedTerminator2.jpg', 'wb')
            file.write(data)
            file.close()
            print('received file')
        else:
            print(response)


def main():
    client = Client()
    client.runs()

if __name__ == "__main__":
    main()

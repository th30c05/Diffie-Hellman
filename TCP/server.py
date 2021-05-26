import socketserver
from base64 import b64decode


class Handler_TCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} sent:".format(self.client_address[0]))
        self.data = b64decode(self.data.decode("utf-8"))

        print(str(self.data).removeprefix("b'").removesuffix("'"))
        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())


def main(HOST, PORT):
    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()


if __name__ == "__main__":
    main(input("Host: "), int(input("Port: ")))

import threading
import socketserver
from base64 import b64encode, b64decode
import socket

b = threading.Barrier(2, timeout=1)


class Handler_TCPServer(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} sent:".format(self.client_address[0]))
        self.data = b64decode(self.data.decode("utf-8"))

        print(str(self.data).removeprefix("b'").removesuffix("'"))
        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())


def server():
    HOST, PORT = "10.0.0.1", 9999
    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()


def send_TCP(data_to_send, host, port):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host, port))
        tcp_client.sendall(data_to_send)
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()
    return received


def client():
    host_ip, server_port = str(input("Host: ")), int(input("Port: "))
    b.wait(1)
    while True:
        data = input("MSG: ")
        data_encoded = b64encode(data.encode("utf-8"))
        received = send_TCP(data_encoded, host_ip, server_port)

        print("Bytes Sent: {}".format(data))
        print("Bytes Received: {}".format(received.decode()))


def server_start():
    t = threading.Thread(target=server())
    t.start()


def client_start():
    t = threading.Thread(target=client())
    t.start()


def main():
    client_start()
    server_start()


if __name__ == '__main__':
    main()

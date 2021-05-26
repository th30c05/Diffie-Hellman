import socket
from base64 import b64encode


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


def main():
    host_ip, server_port = str(input("Host: ")), int(input("Port: "))

    while True:
        data = input("MSG: ")
        data_encoded = b64encode(data.encode("utf-8"))
        received = send_TCP(data_encoded, host_ip, server_port)

        print("Bytes Sent: {}".format(data))
        print("Bytes Received: {}".format(received.decode()))


if __name__ == '__main__':
    main()

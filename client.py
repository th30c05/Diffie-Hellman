import socket
from base64 import b64encode, b64decode
from json import dumps

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.dh import DHParameterNumbers, DHPublicNumbers


def packaging(Header, Data):
    pack1 = ['header', 'data']
    pack2 = (Header, Data)

    pack = dumps(dict(zip(pack1, pack2)))

    pack_b64 = b64encode(pack.encode("utf-8"))
    return pack_b64


def send_TCP(data_to_send, host, port):
    global received
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host, port))
        tcp_client.sendall(data_to_send)

        received = tcp_client.recv(1024, )
        received = str(b64decode(received.decode("utf-8"))).removeprefix("b'").removesuffix("'")

    finally:
        tcp_client.close()
        return received


def AES_key_gen(host, port):
    parameters = DHParameterNumbers(
        int('62613E24191987AD722016A7CD726ADA3C2B386999AF8342910233A49E11BEC95D16F4A9410B259EDCFE8BB65F63D1073BE537254D37C38247EA3BB9BD69F80EF',
            16),
        2).parameters(default_backend())

    private_key = parameters.generate_private_key()

    received = send_TCP(packaging('NewKey', hex(private_key.public_key().public_numbers().y)), host, port)

    shared_key = private_key.exchange(
        DHPublicNumbers(int(received, 16), parameters.parameter_numbers()).public_key(default_backend()))

    return shared_key


def main():
    host_ip, server_port = str(input("Host: ")), int(input("Port: "))
    # host_ip, server_port = "192.168.1.15", 9999

    while True:
        data = input("MSG: ")
        if data == "NewKey":
            shared_key = AES_key_gen(host_ip, server_port)
            print(shared_key)

        else:
            received = send_TCP(packaging("Data", data), host_ip, server_port)
            print("Bytes Sent: {}".format(data))
            print("Response: {}".format(received))


if __name__ == '__main__':
    main()

import socket
from base64 import b64encode, b64decode
from json import dumps

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric.dh import generate_parameters


def send_TCP(data_to_send, host, port):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host, port))
        tcp_client.sendall(data_to_send)
        received = tcp_client.recv(1024)
        received = str(b64decode(received.decode("utf-8"))).removeprefix("b'").removesuffix("'")
    finally:
        tcp_client.close()

    return received


def AES_key_gen(host, port):
    parameters = generate_parameters(generator=2, key_size=512, backend=default_backend())
    p = parameters.parameter_numbers().p
    private_key = parameters.generate_private_key()
    peer_public_key = private_key.public_key()

    pub_key = peer_public_key.public_numbers().y

    json_k = ['header', 'data']
    json_v = ['NewKey']
    json_vv = [pub_key, p]
    package = dumps(dict(zip(json_k, (json_v, json_vv))))

    received = send_TCP(b64encode(package.encode("utf-8")), host, port)

    b_peer_public_key = dh.DHPublicNumbers(int(received), parameters.parameter_numbers()).public_key(
        backend=default_backend())
    shared_key = private_key.exchange(b_peer_public_key)

    return shared_key


def main():
    host_ip, server_port = str(input("Host: ")), int(input("Port: "))
    # host_ip, server_port = "192.168.1.15", 9999

    while True:
        AES_key_gen(host_ip, server_port)
        data = input("MSG: ")

        json_k = ['header', 'data']
        json_v = ['NewKey', data]

        data = dumps(dict(zip(json_k, json_v)))

        data_encoded = b64encode(data.encode("utf-8"))

        received = send_TCP(data_encoded, host_ip, server_port)

        print("Bytes Sent: {}".format(data))
        print("Bytes Received: {}".format(received))


if __name__ == '__main__':
    main()

import socket
from base64 import b64encode, b64decode
from hashlib import sha512
from json import dumps, loads
from secrets import SystemRandom


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

        received = str(b64decode(tcp_client.recv(1024, ).decode("utf-8"))).removeprefix("b'").removesuffix("'")

    finally:
        tcp_client.close()
        return received


def AES_key_gen(host, port):
    random = SystemRandom()

    Prime = int(
        'B858D48846EAD8AA352411841C7A947CCC804B75B953E2703B2B9',
        16)

    Base = 2

    Secret = random.randint(int(
        '26E4D30ECCC3215DD8F3157D27E23ACBDCFE68000000000000000',
        16), int(
        '184F03E93FF9F4DAA797ED6E38ED64BF6A1F00FFFFFFFFFFFFFFFF',
        16))  # a

    public_key = pow(Base, Secret, Prime)

    package = send_TCP((packaging('NewKey', public_key)), host, port)

    # Load json
    package = loads(package)
    shared_key = sha512(str(pow(package['data'], Secret, Prime)).encode('UTF-8')).digest()

    return shared_key


def main():
    # host_ip, server_port = str(input("Host: ")), int(input("Port: "))
    host_ip, server_port = "192.168.1.15", 9999

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

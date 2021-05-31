from base64 import b64encode, b64decode
from json import dumps, loads
from secrets import SystemRandom
from socket import socket, AF_INET, SOCK_STREAM


def packaging(Header, Data):
    pack1 = ['header', 'data']
    pack2 = (Header, Data)

    pack = dumps(dict(zip(pack1, pack2)))

    pack_b64 = b64encode(pack.encode("utf-8"))
    return pack_b64


def send_TCP(data_to_send, host, port):
    global received
    tcp_client = socket(AF_INET, SOCK_STREAM)

    try:
        # Establish connection to TCP server and exchange data
        tcp_client.connect((host, port))
        tcp_client.sendall(data_to_send)

        received = str(b64decode(tcp_client.recv(1024, ).decode("utf-8"))).removeprefix("b'").removesuffix("'")

    finally:
        tcp_client.close()
        return received


def AES_key_gen(host, port):
    while True:
        random = SystemRandom()

        # Set Base and the Prime
        Base = 2
        Prime = int(
            'F32D6D650FB74CDD13F737E5B8C48757325630FA755FAA91D1539',
            16)

        # Generate Secret
        Secret = random.randint(int(
            '26E4D30ECCC3215DD8F3157D27E23ACBDCFE68000000000000000',
            16), int(
            '184F03E93FF9F4DAA797ED6E38ED64BF6A1F00FFFFFFFFFFFFFFFF',
            16))

        # Send the request with the pub key
        package = send_TCP((packaging('NewKey', pow(Base, Secret, Prime))), host, port)

        # Load json
        package = loads(package)

        # Generate the shared key
        shared_key = bytes(str(pow(package['data'], Secret, Prime)), 'UTF-8')
        if len(shared_key) == 64:
            break

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

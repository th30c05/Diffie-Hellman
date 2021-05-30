from _thread import start_new_thread
from base64 import b64decode, b64encode
from hashlib import sha512
from json import dumps, loads
from secrets import SystemRandom
from socket import socket, AF_INET, SOCK_STREAM
from threading import Lock

print_lock = Lock()


def packaging(Header, Data):
    pack1 = ['header', 'data']
    pack2 = (Header, Data)

    pack = dumps(dict(zip(pack1, pack2)))

    pack_b64 = b64encode(pack.encode("utf-8"))
    return pack_b64


def threaded(c):  # thread function

    while True:

        # data received from client
        data = bytes(c.recv(1024))

        if data == b'':
            print_lock.release()
            break

        else:
            # data decoded from base 64 and remove bytes prefix and sufix
            data_decoded = str(b64decode(data.decode("utf-8"))).removeprefix("b'").removesuffix("'")

            # Load json
            package = loads(data_decoded)

            if package['header'] == 'NewKey':  # Detect if is a NewKey request

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

                # Send the public key
                c.send(packaging('NewKey', public_key))

                # Load client PUB key
                shared_key = sha512(str(pow(package['data'], Secret, Prime)).encode('UTF-8')).digest()
                print(shared_key)

            else:
                # Print data and send OK
                print(package['data'])
                c.send(b64encode("200 OK".encode("utf-8")))

    c.close()


def main():
    # host, port = str(input("Host: ")), int(input("Port: "))
    host, port = "192.168.1.15", 9999

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    print("socket is listening")

    while True:
        s.listen(0)

        # a forever loop until client wants to exit
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))


if __name__ == '__main__':
    main()

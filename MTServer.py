from _thread import start_new_thread
from base64 import b64decode, b64encode
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
    global shared_key

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
                while True:
                    random = SystemRandom()

                    Prime = int(
                        'F32D6D650FB74CDD13F737E5B8C48757325630FA755FAA91D1539',
                        16)

                    Base = 2

                    Secret = random.randint(int(
                        '26E4D30ECCC3215DD8F3157D27E23ACBDCFE68000000000000000',
                        16), int(
                        '184F03E93FF9F4DAA797ED6E38ED64BF6A1F00FFFFFFFFFFFFFFFF',
                        16))  # a

                    public_key = pow(Base, Secret, Prime)

                    # Load client PUB key
                    shared_key = bytes(str(pow(package['data'], Secret, Prime)), 'UTF-8')

                    if len(shared_key) == 64:
                        # Send the public key
                        c.send(packaging('NewKey', public_key))
                        break

            else:
                # Print data and send OK
                c.send(b64encode("200 OK".encode("utf-8")))
                print(package['data'])

    c.close()


def main():
    host, port = str(input("Host: ")), int(input("Port: "))
    # host, port = "192.168.1.15", 9999

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    print("socket is listening")
    s.listen(0)

    while True:
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

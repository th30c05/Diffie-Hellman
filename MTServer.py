from _thread import start_new_thread
from base64 import b64decode, b64encode
from json import loads
from socket import socket, AF_INET, SOCK_STREAM
from threading import Lock

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.dh import DHPublicNumbers, DHParameterNumbers

print_lock = Lock()


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

                # Create DH paramaters
                parameters = DHParameterNumbers(
                    int('62613E24191987AD722016A7CD726ADA3C2B386999AF8342910233A49E11BEC95D16F4A9410B259EDCFE8BB65F63D1073BE537254D37C38247EA3BB9BD69F80EF',
                        16),
                    2).parameters(default_backend())

                # Generate new key
                private_key = parameters.generate_private_key()

                # Send the public key
                c.send(b64encode(hex(private_key.public_key().public_numbers().y).encode("utf-8")))

                # Load client PUB key
                b_peer_public_key = DHPublicNumbers(int(package['data'], 16),
                                                    parameters.parameter_numbers()).public_key(default_backend())

                # Generate shared key
                shared_key = private_key.exchange(b_peer_public_key)

            else:
                # Print data and send OK
                print(package['data'])
                c.send(b64encode("200 OK".encode("utf-8")))

    c.close()


def main():
    host, port = str(input("Host: ")), int(input("Port: "))
    # host, port = "192.168.1.15", 9999

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

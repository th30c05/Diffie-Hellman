import socket
import threading
from _thread import *
from base64 import b64decode, b64encode
from json import loads

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh

print_lock = threading.Lock()


def threaded(c):  # thread function

    while True:

        # data received from client
        data = bytes(c.recv(1024))

        # data decoded from base 64 and remove bytes prefix and sufix
        data_decoded = str(b64decode(data.decode("utf-8"))).removeprefix("b'").removesuffix("'")

        if data_decoded == "":
            # Break if no data
            print_lock.release()
            break

        else:
            # Load json
            package = loads(data_decoded)

        if package['header'][0] == 'NewKey':  # Detect if is a NewKey request

            # Create DH paramaters
            parameters = dh.DHParameterNumbers((package['data'])[1], 2)
            parameters = parameters.parameters(default_backend())

            # Generate new key
            private_key = parameters.generate_private_key()

            # Generate and encode public key with base64
            peer_public_key = private_key.public_key()
            a_pub_key = b64encode(str(peer_public_key.public_numbers().y).encode("utf-8"))

            # Send the public key
            c.send(a_pub_key)

            # Load client PUB key
            b_peer_public_key = dh.DHPublicNumbers(package['data'][0], parameters.parameter_numbers()).public_key(
                default_backend())

            # Generate shared key
            shared_key = private_key.exchange(b_peer_public_key)
            print(shared_key)

        else:
            # Print data and send ACK
            print(data_decoded)
            c.send(b64encode("ACK".encode("utf-8")))

    # Connection closed
    c.close()


def Main():
    host = "192.168.1.15"
    port = 9999

    # reverse a port on your computer
    # in our case it is 9999 but it
    # can be anything
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))

    s.close()


if __name__ == '__main__':
    Main()

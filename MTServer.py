from _thread import start_new_thread
from socket import socket, AF_INET, SOCK_STREAM
from textwrap import indent
from threading import Lock

from functions import decrypt
from functions import depackaging
from functions import get_secret
from functions import packaging

print_lock = Lock()


def threaded(c, debug):  # thread function
    global shared_key

    while True:

        # data received from client
        try:
            data = bytes(c.recv(1024))
        except:
            c.close()
            print_lock.release()
            break
        else:
            if data == b'':
                c.close()
                print_lock.release()
                break


            package = depackaging(data)

            if package['header'] == 'NewKey':  # Detect if is a NewKey request
                while True:

                    Base, Prime, Secret, Pub = get_secret()

                    # Load client PUB key
                    shared_key = bytes(str(pow(package['data'], Secret, Prime)), 'UTF-8')

                    if len(shared_key) == 64:
                        if debug:
                            print(indent('Key: ' + str(shared_key), '  '))

                        # Send the public key
                        c.send(packaging('NewKey', Pub))
                        break

            else:
                data = decrypt(shared_key, bytes.fromhex((package['data'])['nonce']), bytes.fromhex(
(package['data'])['ciphertext']), bytes.fromhex((package['data'])['tag'])).decode('UTF-8')
                print(indent("Data: " + data + "\n", "  "))


def main():
    debug = input("Debug? (Y or N) ").upper()
    if debug == "Y":
        debug = True
    else:
        debug = False

    host, port = str(input("Host: ")), int(input("Port: "))

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    print("\nSocket binded to port", port, "\nSocket is listening \n")
    s.listen(0)

    while True:
        # a forever loop until client wants to exit
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Conexion from:', addr[0], 'By port number:', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c, debug,))


if __name__ == '__main__':
    main()

from json import loads
from socket import socket, AF_INET, SOCK_STREAM
from textwrap import indent
from time import sleep

from functions import depackaging
from functions import get_secret
from functions import packaging, encrypt


def create_TCP(host, port):
    tcp_client = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            tcp_client.connect((host, port))

        except:
            print("Error can't connect to " + host + ":" + str(port))
            sleep(1)

        else:
            return tcp_client


def send_TCP(data_to_send, tcp_client):
    tcp_client.send(data_to_send)

    received = tcp_client.recv(1024, ).decode("utf-8")
    return received


def AES_key_gen(host, port):
    while True:

        Base, Prime, Secret, Pub = get_secret()

        tcp_client = create_TCP(host, port)

        package = depackaging(send_TCP((packaging('NewKey', Pub)), tcp_client))

        # Generate the shared key
        shared_key = bytes(str(pow(package['data'], Secret, Prime)), 'UTF-8')
        if len(shared_key) == 64:
            break

    return shared_key, tcp_client


def main():
    debug = input("Debug? (Y or N) ").upper()
    if debug == "Y":
        debug = True
    else:
        debug = False

    host, port = str(input("Host: ")), int(input("Port: "))

    while True:

        data = 'aa'  # input("MSG: ")

        shared_key, tcp_client = AES_key_gen(host, port)

        if debug:
            print('  Key: ', end="")
            print(shared_key)

        package = packaging("Data", loads(encrypt(shared_key, data.encode('UTF-8'))))
        tcp_client.send(package)
        print(indent("Bytes Sent: {} \n".format(data), "  "))
        tcp_client.close()


if __name__ == '__main__':
    main()

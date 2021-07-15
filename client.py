def create_TCP(host, port):
    from socket import socket, AF_INET, SOCK_STREAM
    tcp_client = socket(AF_INET, SOCK_STREAM)

    try:
        tcp_client.connect((host, port))

    except:
        print("Error can't connect to " + host + ":" + port)

    else:
        return tcp_client


def send_TCP(data_to_send, tcp_client):
    tcp_client.send(data_to_send)

    received = tcp_client.recv(1024, ).decode("utf-8")
    return received


def AES_key_gen(host, port):
    while True:

        from functions import get_secret
        Base, Prime, Secret, Pub = get_secret()

        tcp_client = create_TCP(host, port)

        from functions import packaging, depackaging
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

    host_ip, server_port = str(input("Host: ")), int(input("Port: "))

    while True:

        data = input("MSG: ")

        shared_key, tcp_client = AES_key_gen(host_ip, server_port)

        if debug: print(shared_key)

        from functions import packaging, encrypt
        from json import loads
        package = packaging("Data", loads(encrypt(shared_key, data.encode('UTF-8'))))
        tcp_client.send(package)
        print("Bytes Sent: {}".format(data))
        tcp_client.close()


if __name__ == '__main__':
    main()

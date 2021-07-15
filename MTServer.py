from threading import Lock

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

            from functions import depackaging
            package = depackaging(data)

            if package['header'] == 'NewKey':  # Detect if is a NewKey request
                while True:
                    from functions import get_secret

                    Base, Prime, Secret, Pub = get_secret()

                    # Load client PUB key
                    shared_key = bytes(str(pow(package['data'], Secret, Prime)), 'UTF-8')

                    if len(shared_key) == 64:
                        if debug: print(shared_key)

                        # Send the public key
                        from functions import packaging
                        c.send(packaging('NewKey', Pub))
                        break

            else:
                nonce, ciphertext, tag = bytes.fromhex((package['data'])['nonce']), bytes.fromhex(
                    (package['data'])['ciphertext']), bytes.fromhex((package['data'])['tag'])
                from functions import decrypt
                data = decrypt(shared_key, nonce, ciphertext, tag).decode('UTF-8')
                print(data)


def main():
    debug = input("Debug? (Y or N) ").upper()
    if debug == "Y":
        debug = True
    else:
        debug = False

    host, port = str(input("Host: ")), int(input("Port: "))

    from socket import socket, AF_INET, SOCK_STREAM
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
        from _thread import start_new_thread
        start_new_thread(threaded, (c, debug,))


if __name__ == '__main__':
    main()

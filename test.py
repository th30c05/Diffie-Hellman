import base64
from lzma import *

"""
@jit(forceobj=True)
def main():
    key_parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())

    a_private_key = key_parameters.generate_private_key()
    a_peer_public_key = a_private_key.public_key()

    b_private_key = key_parameters.generate_private_key()
    b_peer_public_key = b_private_key.public_key()

    a_shared_key = a_private_key.exchange(b_peer_public_key)
    b_shared_key = b_private_key.exchange(a_peer_public_key)

    print('a_secret: ' + str(a_shared_key))
    print('b_secret: ' + str(b_shared_key))
"""


def main():
    # Program to check if a number is prime or not

    num = '35827166471799293901187590011469386458700646222597313289239616663581878231607847670865366492473226107023909051440722985247671490277488547367298888836712899'
    num = base64.b64encode(num)
    compressor = LZMACompressor(FORMAT_XZ, CHECK_SHA256)
    hello = compressor.compress(bytes(num))
    print(hello)
    # To take input from the user
    # num = int(input("Enter a number: "))


if __name__ == "__main__":
    main()

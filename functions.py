from json import dumps
from json import loads
from random import SystemRandom

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def packaging(Header, Data):
    pack1, pack2 = ['header', 'data'], [Header, Data]

    Package = dumps(dict(zip(pack1, pack2))).encode('UTF-8')

    return Package


def depackaging(Package):
    pack = loads(Package)

    return pack


def get_secret():
    random = SystemRandom()

    Prime, Base, Secret = int('F32D6D650FB74CDD13F737E5B8C48757325630FA755FAA91D1539', 16), 2, random.randint(
        int('26E4D30ECCC3215DD8F3157D27E23ACBDCFE68000000000000000', 16),
        int('184F03E93FF9F4DAA797ED6E38ED64BF6A1F00FFFFFFFFFFFFFFFF', 16))

    Pub = pow(Base, Secret, Prime)

    return Base, Prime, Secret, Pub


def encrypt(Key, Data):
    nonce = get_random_bytes(64)

    cipher = AES.new(Key, AES.MODE_SIV, nonce)
    ciphertext, tag = cipher.encrypt_and_digest(Data)

    json_k, json_v = ['nonce', 'ciphertext', 'tag'], [nonce.hex(), ciphertext.hex(), tag.hex()]

    result = dumps(dict(zip(json_k, json_v))).encode('UTF-8')

    return result


def decrypt(key, nonce, ciphertext, tag):
    cipher = AES.new(key=key, mode=AES.MODE_SIV, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    return data

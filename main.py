from primatives.sym_keyed_primatives.block_ciphers import IDEA
from random import getrandbits
from PIL import Image
from functions import *
from encryption import *

def main():

    key = 0xedb162c0f8b7778d76829edb6a74494

    i = IDEA(key)

    p = b"0"
    c = encrypt(key, p, 'IDEA')
    d = decrypt(key, c, "IDEA")
    print(p, c, d)


if __name__ == '__main__':
    main()

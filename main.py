from primatives.sym_keyed_primatives.block_ciphers import IDEA
from random import getrandbits
from PIL import Image
from functions import *

def main():

    key = 0xedb162c0f8b7778d76829edb6a74494

    i = IDEA(key)

    p = b"12345678and mad scientists"
    c = encrypt(p, i.encrypt_block, 64)
    d = decrypt(c, i.decrypt_block, 64)
    print(p,c,d)


if __name__ == '__main__':
    main()

from primatives.sym_keyed_primatives.block_ciphers import IDEA
from random import getrandbits
from PIL import Image
from functions import *

def main():

    key = 0xedb162c0f8b7778d76829edb6a74494

    i = IDEA(key)

    p = string_to_bytes("hello")
    print(p)
    c = i.encrypt(p)
    print(c)
    d = i.decrypt(c)
    print(d)

if __name__ == '__main__':
    main()

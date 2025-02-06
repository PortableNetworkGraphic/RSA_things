from functions import *
from primatives.sym_keyed_primatives.block_ciphers import IDEA
from random import getrandbits

def main():
    p = encode_string_to_bits("hello")
    k = getrandbits(p.bit_length())

    c = IDEA(k).encrypt(p)
    print(c)
    print(decode_bits_to_string(IDEA(k).decrypt(c)))


if __name__ == '__main__':
    main()

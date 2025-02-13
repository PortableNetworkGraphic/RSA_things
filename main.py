from secrets import randbits

from functions import *
from primatives.sym_keyed_primatives.block_ciphers import AES
from random import getrandbits, random


def main():

    key = 181901790505226098135696675519197758418

    print(AES.ShiftRows(0x32C1D6F2A7F91E7634BA9C8D4F251D68))


if __name__ == '__main__':
    main()

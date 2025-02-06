from functions import *
from RSA import *
from time import perf_counter as pc
from primatives.sym_keyed_primatives.stream_ciphers import one_time_pad
from primatives.sym_keyed_primatives.block_ciphers import IDEA

def main():
    m = 0b11011110011011011010
    k = 0b10011001010101010101

    one_time_pad(k).



if __name__ == '__main__':
    main()

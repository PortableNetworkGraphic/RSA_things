from math import ceil
from pydoc import plain

from functions import *

class IDEA:

    def __init__(self, key: int, key_size: int=128):
        assert  0 <= key < 2**key_size, "Class = IDEA, Function = __init__: Key must be between 0 and 2**128"
        self.key = key
        self.subkeys = self.gen_subkeys()
        self.deckeys = self.inverse_gen_keys()

    @staticmethod
    def mul_inv(Z: int):
        """
        Computes the multiplicative inverse of Z mod 65537 using Extended Euclidean Algorithm.
        Created by ChatGPT bc I don't know what the hell this means.

        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        """
        if Z == 0:
            return 65536  # IDEA treats 0 as 65536
        Z = Z % 65537  # Ensure Z is within mod space
        t, new_t = 0, 1
        r, new_r = 65537, Z

        while new_r != 0:
            quotient = r // new_r
            t, new_t = new_t, t - quotient * new_t
            r, new_r = new_r, r - quotient * new_r

        if r > 1:
            raise ValueError("Z has no multiplicative inverse mod 65537")
        if t < 0:
            t += 65537  # Ensure positive result

        return t

    @staticmethod
    def mul_mod(a, b):
        assert 0 <= a <= 0x10000
        assert 0 <= b <= 0x10000


        if a == 0:
            a = 0x10000
        if b == 0:
            b = 0x10000

        r = (a * b) % 0x10001

        if r == 0x10000:
            r = 0

        assert 0 <= r <= 0xFFFF
        return r

    def gen_subkeys(self):

        subkeys = []
        key = self.key

        while len(subkeys) < 52:

            for i in range(8):
                subkeys.append((key >> (112 - i * 16)) & 0xFFFF)

            key = rotate(key, 128, 25)

        subkeys = [subkeys[i:i+6] for i in range(0, 54, 6)]

        return subkeys[:8]+[subkeys[8][:4]]

    def inverse_gen_keys(self):

        deckeys = [[0]*6 for _ in range(8)]+[[0]*4]

        deckeys[8][0] = self.mul_inv(self.subkeys[0][0])
        deckeys[8][1] = self.mul_inv(self.subkeys[0][1])
        deckeys[8][2] = (-self.subkeys[0][2]) & 0xFFFF
        deckeys[8][3] = (-self.subkeys[0][3]) & 0xFFFF

        for i in range(8):
            deckeys[i][0] = self.mul_inv(self.subkeys[8 - i][0])
            deckeys[i][1] = self.mul_inv(self.subkeys[8 - i][1])
            deckeys[i][2] = (-self.subkeys[8 - i][2]) & 0xFFFF
            deckeys[i][3] = (-self.subkeys[8 - i][3]) & 0xFFFF
            deckeys[i][4] = self.subkeys[7 - i][4]
            deckeys[i][5] = self.subkeys[7 - i][5]

        return deckeys

    def full_round(self, X1, X2, X3, X4, Z1, Z2, Z3, Z4, Z5, Z6):

        S1 = self.mul_mod(X1, Z1)

        S2 = self.mul_mod(X2, Z2)

        S3 = (X3 + Z3) % 0x10000

        S4 = (X4 + Z4) % 0x10000

        S5 = S1 ^ S3

        S6 = S2 ^ S4

        S7 = self.mul_mod(S5, Z5)

        S8 = (S7 + S6) % 0x10000

        S9 = self.mul_mod(S8, Z6)

        S10 = (S7 + S9) % 0x10000

        S11 = S1 ^ S9

        S12 = S3 ^ S9

        S13 = S2 ^ S10

        S14 = S4 ^ S10

        return S11, S13, S12, S14

    def encrypt_block(self, block: int) -> int:

        assert 0 <= block < 2**64, "Block must be integer within the range 0 to 2**64."

        P1, P2, P3, P4 = split_bin(block, 4, 16)

        for i in range(8):
            P1, P2, P3, P4 = self.full_round(P1, P2, P3, P4, *self.subkeys[i])

        P1 = self.mul_mod(P1, self.subkeys[8][0])
        P2 = self.mul_mod(P2, self.subkeys[8][1])
        P3 = (P3 + self.subkeys[8][2]) % 0x10000
        P4 = (P4 + self.subkeys[8][3]) % 0x10000

        return (P1 << 48) | (P2 << 32) | (P3 << 16) | P4

    def decrypt_block(self, block: int) -> int:
        """
        The decrypt function is effectively ideentical to the encrypt function, but uses
        a different set of keys.
        """

        assert 0 <= block < 2**64, "Block must be integer within the range 0 to 2**64."

        P1, P2, P3, P4 = split_bin(block, 4, 16)

        for i in range(8):
            P1, P2, P3, P4 = self.full_round(P1, P2, P3, P4, *self.deckeys[i])

        P1 = self.mul_mod(P1, self.deckeys[8][0])
        P2 = self.mul_mod(P2, self.deckeys[8][1])
        P3 = (P3 + self.deckeys[8][2]) % 0x10000
        P4 = (P4 + self.deckeys[8][3]) % 0x10000

        return concatenate_bin([P1, P2, P3, P4], 16)

    def encrypt(self, binary: int):

        blocks = split_bin(binary, ceil((len(bin(binary))-2)/64), 64)

        encrypted_blocks = []

        for block in blocks:
            encrypted_blocks.append(self.encrypt_block(block))

        return concatenate_bin(encrypted_blocks, 64)

    def decrypt(self, binary: int):

        encrypted_blocks = split_bin(binary, ceil((len(bin(binary))-2)/64), 64)

        decrypted_blocks = []
        for block in encrypted_blocks:
            decrypted_blocks.append(self.decrypt_block(block))

        return concatenate_bin(decrypted_blocks, 64)

class AES:

    SBOX = [
        # 0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    ]

    RCON = [0x00000000, 0x01000000, 0x02000000, 0x04000000,
            0x08000000, 0x10000000, 0x20000000, 0x40000000,
            0x80000000, 0x1b000000, 0x36000000]

    def __init__(self, key: int, key_size: int=128):
        self.key_size = key_size

        assert 0 <= key < 2**self.key_size
        assert self.key_size in [128, 196, 256]

        self.key = key
        self.key_expansion()
        self.round_keys = self.key_expansion()

    @staticmethod
    def RotWord(word: int) -> int:
        return rotate(word, 32,  1)

    @staticmethod
    def SubWord(word: int) -> int:
        return concatenate_bin([AES.SBOX[b] for b in split_bin(word, 4, 16)], 8)

    @staticmethod
    def SubState(state: int) -> int:
        bytes_ = split_bin(state, 16, 8)
        bytes_ = [AES.SBOX[byte>>4][byte&0xF] for byte in bytes_]
        return concatenate_bin(bytes_, 8)

    @staticmethod
    def ShiftRows(state: int) -> int:
        bytes_ = split_bin(state, 4, 32)
        bytes_ = [split_bin(byte, 4, 8) for byte in bytes_]
        [[a, b, c, d], [e, f, g, h], [i, j, k, l], [m, n, o, p]] = bytes_.copy()

        bytes_ = [a,b,c,d],[f,g,h,e],[k,l,i,j],[p,m,n,o]

        print(bytes_)

        bytes_ = concatenate_bin([concatenate_bin(byte, 8) for byte in bytes_], 32)

        print(hex(bytes_))

    def key_expansion(self) -> list:
        assert self.key_size == 128

        round_keys = [0] * 4

        for i in range(len(round_keys)):
            round_keys[i] = self.key >> (128 - 32 * (i+1)) & 2**32-1

        for i in range(4, 44):

            if i % 4 == 0: pass


        return round_keys

    def encrypt_block(self, block: int):
        assert 0 <= block < 2**128

        # Initial Round (Round 0)
        state = block ^ concatenate_bin(self.round_keys[0:3], 32)

        # Main Rounds (Rounds 1-9)

        for i in range(1, 9+1):
            pass

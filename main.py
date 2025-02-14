from primatives.sym_keyed_primatives.block_ciphers import AES

def main():

    key = 181901790505226098135696675519197758418

    aes = AES(key)
    print(hex(key))
    print([[hex(s) for s in d] for d in aes.key])


if __name__ == '__main__':
    main()

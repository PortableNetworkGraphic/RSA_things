from functions import *
from RSA import *
from time import perf_counter as pc

def main():

    message = "hello everybody!"
    message = encode_string_to_bits(message)


    sender = RSA()
    recipient = RSA()

    encrypted_message = sender.encrypt(message, recipient.public)
    signature = sender.sign(message)


    decrypted_message = recipient.decrypt(encrypted_message)
    print(recipient.verify(decrypted_message, signature, sender.public))

    decrypted_message = decode_bits_to_string(decrypted_message)

    print(decrypted_message)


if __name__ == '__main__':
    main()

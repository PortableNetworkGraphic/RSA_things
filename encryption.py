from functions import *
from primatives.sym_keyed_primatives.block_ciphers import method_info as bc_methods
from primatives.sym_keyed_primatives.stream_ciphers import method_info as sc_methods

methods = bc_methods | sc_methods

def encrypt(key, plainbytes: bytes, method_name: str) -> bytes:

    method = methods[method_name]
    instance = method["class"](key)
    encryption_function = method["encrypt"]
    block_size = method["blocksize"]


    if method["type"] == "block":
        blocks = split_bytes(plainbytes, block_size // 8)

        encrypted_blocks = []
        for block in blocks:
            encrypted_blocks.append(encryption_function(instance, block))

        return concatenate_bytes(encrypted_blocks, block_size // 8)
    else:
        return plainbytes

def decrypt(key, cipherbytes: bytes, method_name: str) -> bytes:

    method = methods[method_name]
    instance = method["class"](key)
    decryption_function = method["decrypt"]
    block_size = method["blocksize"]


    if method["type"] == "block":
        blocks = split_bytes(cipherbytes, block_size // 8)

        decrypted_blocks = []
        for block in blocks:
            decrypted_blocks.append(decryption_function(instance, block))

        return concatenate_bytes(decrypted_blocks, block_size // 8)
    else:
        return cipherbytes
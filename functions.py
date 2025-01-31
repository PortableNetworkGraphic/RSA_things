import sympy

def rotate(num: int, numsize: int, bits: int) -> int:
    """
    I don't know if this function will work for negative numbers or lengths above numsize. I don't want to find out.
    """
    assert 0 < bits < numsize, "rotate: Bits to rotate must be a natural number below numsize."
    assert 0 <= num < (1 << numsize), "rotate: Rotated number must be between 0 and 2**128."
    return ((num << bits) | (num >> (numsize-bits))) & ((1 << numsize)-1)

def split_bin(num: int, divisors: int, divisor_size: int=16) -> list:
    nums = []

    for i in range(divisors-1, -1, -1):
        nums.append((num >> i*divisor_size) & (2**divisor_size-1))

    return nums

def concatenate_bin(nums: list, divisor_size: int=16) -> int:
    num = 0
    for count, piece in enumerate(nums):
        num = num | (piece << (divisor_size*(len(nums)-count-1)))

    return num

def encode_string_to_bytes(string: str) -> bytes:
    return string.encode(encoding='utf-8')

def encode_bytes_to_bits(byte: bytes) -> int:
    return int.from_bytes(byte, byteorder='big')

def encode_string_to_bits(string: str) -> int:
    return encode_bytes_to_bits(encode_string_to_bytes(string))

def decode_bits_to_bytes(bits: int) -> bytes:
    return bits.to_bytes((bits.bit_length()+7)//8, byteorder="big")

def decode_bytes_to_string(byte: bytes) -> str:
    return byte.decode('utf-8')

def decode_bits_to_string(bits: int) -> str:
    return decode_bytes_to_string(decode_bits_to_bytes(bits))


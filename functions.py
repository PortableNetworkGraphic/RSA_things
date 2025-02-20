from PIL import Image


def rotate(num: int, numsize: int, bits: int) -> int:
    """
    I don't know if this function will work for negative numbers or lengths above numsize. I don't want to find out.
    """
    assert 0 < bits < numsize, "rotate: Bits to rotate must be a natural number below numsize."
    assert 0 <= num < (1 << numsize), "rotate: Rotated number must be between 0 and 2**128."
    return ((num << bits) | (num >> (numsize-bits))) & ((1 << numsize)-1)

def pad_byte(data: bytes, block_size: int=8) -> bytes:
    pad_len = (block_size - (len(data) % block_size)) % block_size
    return data + bytes([pad_len] * pad_len)

def unpad_byte(data: bytes, block_size: int=8) -> bytes:
    assert 0 < len(data) <= block_size, "How? what the?"
    pad_len = data[-1]
    if not 0 < pad_len < block_size: return data

    return data[:-pad_len] if pad_len < block_size else data


def split_bin(num: int, blocks: int, block_size: int=16) -> list[int]:
    nums: list[int] = []

    for i in range(blocks - 1, -1, -1):
        nums.append((num >> i * block_size) & (2 ** block_size - 1))

    return nums

def concatenate_bin(nums: list, block_size: int=16) -> int:
    num = 0
    for count, piece in enumerate(nums):
        num = num | (piece << (block_size * (len(nums) - count - 1)))

    return num

def split_bytes(data: bytes, block_size: int) -> list[bytes]:

    return [pad_byte(data[i: i + block_size], block_size) for i in range(0, len(data), block_size)]

def concatenate_bytes(data: list[bytes], block_size: int) -> bytes:

    data = b''.join([unpad_byte(b) for b in data])

    return data

def string_to_bytes(string: str) -> bytes:
    return string.encode(encoding='utf-8')

def bytes_to_bits(byte: bytes) -> int:
    return int.from_bytes(byte, byteorder='big')

def string_to_bits(string: str) -> int:
    return bytes_to_bits(string_to_bytes(string))

def bits_to_bytes(bits: int) -> bytes:
    return bits.to_bytes((bits.bit_length()+7)//8, byteorder="big")

def bytes_to_string(byte: bytes) -> str:
    return byte.decode('utf-8')

def bits_to_string(bits: int) -> str:
    return bytes_to_string(bits_to_bytes(bits))

def as_list(x):
    if type(x) in [list, tuple]:
        return x
    else:
        return [x]

def apply_function_to_each_pixel_of_an_image(image: Image.Image, function) -> Image.Image:

    image = image.copy()

    width, height = image.size

    for y in range(height):
        for x in range(width):
            b = image.getpixel((x, y))
            new_val = tuple(function(v) for v in as_list(b))
            image.putpixel((x, y), new_val)

    return image

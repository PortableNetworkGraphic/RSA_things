from primatives.sym_keyed_primatives.block_ciphers import IDEA
from random import getrandbits
from PIL import Image
from functions import *

def main():

    key = 0xedb162c0f8b7778d76829edb6a74494

    I = IDEA(key)

    img = Image.open("one_time_clam.png")
    img = img.convert("L")
    width, height = img.size

    img = apply_function_to_each_pixel_of_an_image(img, lambda x: 255-x)

    b = image_to_blocks(img, 64)
    print(len(b))



if __name__ == '__main__':
    main()

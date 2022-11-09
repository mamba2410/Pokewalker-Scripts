import PIL
from PIL import Image
from txt_to_bin import *
from img_to_txt import *
from slice_image import *
import numpy as np

def img_to_bin(in_file: Image, width: int, height: int, frames: int) -> bytearray:
    data = np.array(bytearray(in_file.convert('L').tobytes()), dtype='uint8')
    #n_bytes = len(data)
    n_bytes = in_file.width*in_file.height

    out = np.zeros(n_bytes//4, dtype='uint8')

    data = ((data>>6)&3)    ## get top 2 bits
    for i in range(n_bytes):
        row = i//width
        col = i%width

        bitpos = row%8
        bitrow = row//8

        pw_index = 2*(bitrow*width + col)

        out[pw_index+0] |= ((data[i]&2)>>1) << bitpos
        out[pw_index+1] |= (data[i]&1) << (bitpos)

    out_bytes = bytearray(out)
    return out_bytes



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Correct syntax: img_to_bin.py in-file out-file")
        sys.exit()

    with Image.open(sys.argv[1]) as in_file:
        with open(sys.argv[2], "wb") as out_file:
            out_file.write(img_to_bin(in_file))

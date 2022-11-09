import sys
from PIL import Image

"""
Accepts PW-style bytes, returns correctly encoded Image
"""
def bin_to_img(in_bin, width=64, height=48, frames=2, inverted=False):
    if inverted:
        data = bytes([b ^ 0b11111111 for b in in_bin])
    else:
        data = bytes(in_bin)
    img = Image.frombytes('1', (16, width*height*frames//8), data)
    img = unslice_image(img, width=width, height=height, frames=frames)
    return img

def unslice_image(in_img: Image, width=64, height=48, frames=2):
    if in_img == None:
        return in_img

    in_img = in_img.convert('L')

    lchunks = [in_img.crop((0,in_img.height-((i+1)*width),8,in_img.height-(i*width))) for i in range(height*frames//8)]
    rchunks = [in_img.crop((8,in_img.height-((i+1)*width),16,in_img.height-(i*width))) for i in range(height*frames//8)]

    out_img = Image.new('L', (height*frames,width))

    for i in range(height*frames//8):
        out_img.paste(Image.blend(lchunks[i],rchunks[i],2/3), (i*8, 0))

    return out_img.transpose(Image.ROTATE_90)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Correct syntax: bin_to_img.py in-file")
        sys.exit()
    with open(sys.argv[1], "rb") as in_bin:
        unslice_image(bin_to_img(in_bin.read())).show()

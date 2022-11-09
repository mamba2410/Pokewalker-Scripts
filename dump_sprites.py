import ndspy.narc
import ndspy.lz10
from bin_to_img import *
import os.path

def dump(path, width=64, height=48, frames=2):
    narc = ndspy.narc.NARC.fromFile(path)
    #data = ndspy.lz10.decompress(narc.files[0])

    basename = os.path.basename(path)
    images = []

    for id in range(0, len(narc.files)):
        #unslice_image(bin_to_img(ndspy.lz10.decompress(narc.files[id]))).save("./out/"+str(id)+".png", "PNG")
        fname = f"./out/{basename}_{id}.png"
        data = ndspy.lz10.decompress(narc.files[id])
        img = bin_to_img(data, width=width, height=height, frames=frames, inverted=True)
        img.save(fname, "PNG")
        images.append(img)

        #print(str(id)+": done.")

    return images

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Correct syntax: sprite_dump.py in-file")
        sys.exit()
    dump(sys.argv[1])

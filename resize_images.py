from pathlib import Path

import numpy as np
from PIL import Image


def multi_channel_img_to_multi_scale_img(path):
    # read original 512 image
    image_512 = Image.open(path)

    # resize original 512 image to 128
    image_512_resized_128 = image_512.resize((128, 128))
    image_512_resized_128.save('test_512_resized_128.jpg')

    # get 256 image by cropping original 512
    left, top, right, bottom = 256/2, 256/2, 512 - 256/2, 512 - 256/2
    image_512_cropped_256 = image_512.crop((left, top, right, bottom))
    # image_512_cropped_256.save('test_512_cropped_256.jpg')

    # resize 256 cropped image to 128
    image_256_resized_128 = image_512_cropped_256.resize((128, 128))
    image_256_resized_128.save('test_256_resized_128.jpg')

    # get 128 image by cropping original 512
    left, top, right, bottom = 256/2 + 128/2, 256/2 + \
        128/2, 512 - (256/2 + 128/2), 512 - (256/2 + 128/2)
    image_512_cropped_128 = image_512.crop((left, top, right, bottom))
    image_512_cropped_128.save('test_512_cropped_128.jpg')

    return np.stack([image_512_resized_128, image_256_resized_128, image_512_cropped_128])


if __name__ == "__main__":
    path = Path('extracted-data\imagery\\athina, gr\Agricultural + Semi-natural areas + Wetlands\\athina_z17_s512_37.8891505835_23.4384444463_grid-i0_grid-j23.jpg')
    stacked_images = multi_channel_img_to_multi_scale_img(path)
    print(stacked_images.shape)

# TODO create function that resizes all images in 128, 256 and 512 sizes
# does not only need resize but also cropping for zoom purposes
# concatenate data before
# stack data after
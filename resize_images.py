from PIL import Image
from pathlib import Path

path = Path('extracted-data\imagery\\athina, gr\Agricultural + Semi-natural areas + Wetlands\\athina_z17_37.88915_23.43844_grid-i0_grid-j23.jpg')
image = Image.open(path)

new_image = image.resize((512, 512))
new_image.save('test_512.jpg')
new_image = image.resize((256, 256))
new_image.save('test_256.jpg')
new_image = image.resize((128, 128))
new_image.save('test_128.jpg')


# TODO create function that resizes all images in 128, 256 and 512 sizes
# does not only need resize but also cropping for zoom purposes
# concatenate data before
# stack data after
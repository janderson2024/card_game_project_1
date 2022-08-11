#USED THIS TO RENAME ALL THE IMAGES VERY QUICKLY

import os

to_upper = ["ace", "jack", "queen", "king", "joker", "clubs", "diamonds", "hearts", "spades", "clubs2", "diamonds2", "hearts2", "spades2"]

def get_all_png() -> [str]:
    files = os.listdir()
    images = [file for file in files if file.endswith(".png")]
    return images

for image in get_all_png():
	og_name = image

	without_png = image[:-4]

	parts = without_png.split("_")

	fixed = "_".join([part.capitalize() if part in to_upper else part for part in parts])

	fixed = fixed + ".png"

	print(fixed)

	os.rename(og_name, fixed)
import json
from pathlib import Path
from PIL import Image
import numpy as np

# https://stackoverflow.com/questions/1905421/crop-a-png-image-to-its-minimum-size


def bbox(im):
    a = np.array(im)[:, :, :3]  # keep RGB only
    m = np.any(a != [255, 255, 255], axis=2)
    coords = np.argwhere(m)
    y0, x0, y1, x1 = *np.min(coords, axis=0), *np.max(coords, axis=0)
    return (x0, y0, x1+1, y1+1)


def add_parts_to_img(im, data, puzzle_dir):
    for item in data:
        part = data[item][item]
        if "name" not in part:
            img = Path(puzzle_dir) / (item + '.png')
        else:
            img = Path(puzzle_dir) / (part["name"] + '.png')
        part_img = Image.open(img)
        part_img = part_img.resize((part["width"], part["height"]))
        w2, h2 = part_img.size  # get the width and height of img2
        x_coord = int(part["x"] - (w2 // 2))
        y_coord = int(im.size[1] - part["y"] - (h2 // 2))
        im = paste_image(im, part_img, x_coord, y_coord)
        part_img.close()
    return im

# thanks bing


def paste_image(img1, img2, x, y):
    # img1 is the background image
    # img2 is the image to be pasted
    # x and y are the top left coordinates of the pasted image
    # returns the combined image
    # convert both images to RGBA mode
    img1 = img1.convert('RGBA')
    img2 = img2.convert('RGBA')
    # get the width and height of both images
    w1, h1 = img1.size
    # create a new image with the same size as img1 and transparent background
    layer = Image.new('RGBA', (w1, h1), (0, 0, 0, 0))
    # paste img2 on layer at the desired location
    layer.paste(img2, (x, y))
    # alpha composite layer over img1
    result = Image.alpha_composite(img1, layer)
    # return the result
    return result


def assemble_puzzle(filename, texture_dir, out_dir):
    with open(filename, "r", encoding="UTF-8") as f:
        data = json.load(f)
    Path.mkdir(out_dir, exist_ok=True)
    default_img = None
    largest_x = 0
    largest_y = 0
    for x in data["skins"]:
        for y in data["skins"][x]:
            part = data["skins"][x][y][y]
            value = part["x"] + part["width"]
            if value > largest_x:
                largest_x = value
            value = part["y"] + part["height"]
            if value > largest_y:
                largest_y = value

    im = Image.new('RGBA', (int(largest_x), int(largest_y)),
                   (255, 255, 255, 0))
    for item in data["skins"]:
        im = add_parts_to_img(im, data["skins"][item], texture_dir)
        if item == "default":
            default_img = im.copy()
        im = im.crop(bbox(im))
        im.save(out_dir / f'{item}.png')
        print("Saved combined sprite", item)
        im = default_img.copy()

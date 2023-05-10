from PIL import Image
from pathlib import Path
import sys
from libs.atlas_parser import atlas_parser


def cut_image(im, xy, wh, out_name, rotate):
    Path.mkdir(out_name.parent, exist_ok=True, parents=True)
    if rotate:
        temp_img = im.crop((xy[0], xy[1], xy[0] + wh[1], xy[1] + wh[0]))
        temp_img = temp_img.rotate(-90, expand=True)
    else:
        temp_img = im.crop((xy[0], xy[1], xy[0] + wh[0], xy[1] + wh[1]))
    temp_img.save(out_name)


def extract_sprites(filename):
    print("Extracting sprites...")
    data = atlas_parser(filename)
    directory = Path(filename).parent
    image_dir = directory / (data["tex_name"])
    if image_dir.exists():
        image = Image.open(image_dir)
        alpha_dir = image_dir.parent / f'{data["tex_name"][:-4]}_a.png'
        if alpha_dir.exists():
            im_a = Image.open(alpha_dir).convert('L').resize(image.size)
            image.putalpha(im_a)
    else:
        print("Image not found:", image_dir)
        return

    for part in data["parts"]:
        out_dir = directory / \
            (data["tex_name"][:-4] + "_ext") / (part["name"] + ".png")
        cut_image(image, part["xy"], part["size"],
                  out_dir, rotate=part["rotate"])
    image.close()
    im_a.close()

def main():
    print("\n--RON spriteExtract--\n\nWritten by Timo654.")
    if len(sys.argv) > 1:
        prefab_files = sys.argv[1:]
        for prefab_file in prefab_files:
            extract_sprites(prefab_file)
    else:
        input(
            'You need to drag a prefab file onto the script.\nPress ENTER to continue...\n')


if __name__ == '__main__':
    main()

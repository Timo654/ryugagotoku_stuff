import sys
from pathlib import Path
from libs.spriteExtract import extract_sprites
from libs.puzzle import assemble_puzzle


def handle_file(filename):
    extensions = "".join(Path(filename).suffixes)
    filename = Path(filename.removesuffix(extensions).rstrip("_a"))
    paths = list()
    paths.append(filename.with_suffix(".png"))
    paths.append(filename.parent / f'{filename}_a.png')
    paths.append(filename.with_suffix(".atlas.prefab"))
    paths.append(filename.with_suffix(".prefab"))
    out_path = Path(str(filename) + "_ext")
    for path in paths:  # verify that paths are valid
        if not path.exists():
            input("Make sure you have all the necessary files (.png, _a.png, .prefab and .atlas.prefab). Press ENTER to continue...")
            return
    extract_sprites(paths[2])
    assemble_puzzle(paths[3], out_path, out_path / "combined")


def main():
    print("\n--RONix--\nRGG Online Sprite Extractor/Combiner\nWritten by Timo654.\n")
    if len(sys.argv) > 1:
        prefab_files = sys.argv[1:]
        for prefab_file in prefab_files:
            handle_file(prefab_file)
        input("Done!\nPress ENTER to close.")
    else:
        input('You need to drag a prefab or PNG file onto the script.\nPress ENTER to continue...\n')


if __name__ == '__main__':
    main()

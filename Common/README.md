# Common
Scripts that should work for most games.

**acb_name_dumper** - Reads acb names from the sound file metadata and saves data to an .xlsx file. May work for other games, but I only tested it with Old Engine RGG titles.

**bone(update)r** - Script for copying bone positions from one GMD to another, useful for fixing issues with facial animations.
Tool for copying bone positions from one model to another. Useful for fixing faces easily.

The tool reads the bones that it has to replace from "swap_list.txt" by default. Each line is a new bone. It will look for any bone starting with a specific string, for example "face" would find both "face" and "face_c_n".
Usage:
boner.py -s "MODEL TO COPY BONES FROM" -i "MODEL TO COPY BONES TO"
Optional parameter: -l "TEXT FILE TO READ BONE LIST FROM"
import json
from binary_reader import BinaryReader, Endian
import argparse


def read_file(filename, game):
    print("Reading", filename)
    with open(filename, 'rb') as file:
        mus = BinaryReader(file.read(), Endian.BIG, encoding="shift-jis")
    data = dict()
    data["Game"] = game
    data['Field_0x0'] = mus.read_uint32()
    data['Field_0x4'] = mus.read_uint16()
    item_count = mus.read_uint16()
    item_pointer = mus.read_uint32()
    data["CommonStrings"] = list()
    strCount = (item_pointer - 12) // 4
    for _ in range(strCount):
        pointer = mus.read_uint32()
        with mus.seek_to(pointer):
            data["CommonStrings"].append(mus.read_str())

    data["Items"] = list()
    mus.seek(item_pointer)
    for _ in range(item_count):
        item = dict()
        item["ID"] = mus.read_uint16()
        item["Field_0x2"] = mus.read_uint16()
        item["Price"] = mus.read_uint32()
        item["Field_0x8"] = mus.read_int16() # related to when the item appears in the shop?
        item["Field_0xA"] = mus.read_int16()
        if game != "kenzan":
            item["Field_0xC"] = mus.read_int32() # YAKUZA 3
        with mus.seek_to(mus.read_uint32()):
            item["Description"] = mus.read_str()
        data["Items"].append(item)

    with open(f'{filename}.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_string(head, string_br, string, top_size):
    head.write_uint32(top_size + string_br.pos())
    string_br.write_str(string, null=True)


def rebuild(input_file):
    print("Rebuilding", input_file)
    with open(input_file, encoding='UTF-8') as f:
        data = json.loads(f.read())
    game = data["Game"].lower()
    if game == "kenzan":
        item_data_size = 16 * len(data["Items"]) # 16 if Kenzan
    else:
        item_data_size = 20 * len(data["Items"]) # 20 if Y3

    header_size = 12 + len(data["CommonStrings"])*4
    # header
    head = BinaryReader(endianness=Endian.BIG)
    head.write_uint32(data["Field_0x0"])
    head.write_uint16(data["Field_0x4"])
    head.write_uint16(len(data["Items"]))
    head.write_uint32(header_size)  # item start pos

    string_br = BinaryReader(endianness=Endian.BIG, encoding="shift-jis")
    for string in data["CommonStrings"]:
        write_string(head, string_br, string, item_data_size + header_size)

    for item in data["Items"]:
        head.write_uint16(item["ID"])
        head.write_uint16(item["Field_0x2"])
        head.write_uint32(item["Price"])
        head.write_int16(item["Field_0x8"])
        head.write_int16(item["Field_0xA"])
        if game != "kenzan":
            head.write_int32(item["Field_0xC"]) # YAKUZA 3
        write_string(head, string_br,
                     item["Description"], item_data_size + header_size)
    head.extend(string_br.buffer())

    with open(f'{input_file}.bin', 'wb') as f:
        f.write(head.buffer())


def main():
    print("--MUSASHI SHOPPING 1.1--\n\n")
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--game", default="yakuza3", help="Name of the game. Possible options are 'kenzan' and 'yakuza3'")
    parser.add_argument("files", nargs="*", help="Shop bin/json files")
    args = parser.parse_args()
    if len(args.files) > 0:
        file_count = 0
        for file in args.files:
            if file.endswith(".json"):
                rebuild(file)
            else:
                read_file(file, args.game)
            file_count += 1

        print(f'{file_count} file(s) rebuilt.')
        input("Press ENTER to continue...")
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')


if __name__ == "__main__":
    main()

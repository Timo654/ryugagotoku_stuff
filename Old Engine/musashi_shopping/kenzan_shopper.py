import json
from binary_reader import BinaryReader, Endian
import sys


def read_file(filename):
    print("Reading", filename)
    with open(filename, 'rb') as file:
        mus = BinaryReader(file.read(), Endian.BIG, encoding="shift-jis")
    data = dict()
    data['Field_0x0'] = mus.read_uint32()
    data['Field_0x4'] = mus.read_uint16()
    item_count = mus.read_uint16()
    item_pointer = mus.read_uint32()
    data["CommonStrings"] = list()
    for _ in range(8):
        pointer = mus.read_uint32()
        with mus.seek_to(pointer):
            data["CommonStrings"].append(mus.read_str())

    data["Items"] = list()
    mus.seek(item_pointer)
    for i in range(item_count):
        item = dict()
        item["ID"] = mus.read_uint16()
        item["Field_0x2"] = mus.read_uint16()
        item["Price"] = mus.read_uint32()
        item["Field_0x8"] = mus.read_int16() # related to when the item appears in the shop?
        item["Field_0xA"] = mus.read_int16()
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
    common_string_count = 8
    item_data_size = 16 * len(data["Items"])
    header_size = 12 + common_string_count*4
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
        write_string(head, string_br,
                     item["Description"], item_data_size + header_size)
    head.extend(string_br.buffer())

    with open(f'{input_file}.bin', 'wb') as f:
        f.write(head.buffer())


def main():
    print("--MUSASHI SHOPPING--\n\n")
    if len(sys.argv) > 1:
        input_files = sys.argv[1:]
        file_count = 0
        for file in input_files:
            if file.endswith(".json"):
                rebuild(file)
            else:
                read_file(file)
            file_count += 1

        print(f'{file_count} file(s) rebuilt.')
        input("Press ENTER to continue...")
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')


if __name__ == "__main__":
    main()

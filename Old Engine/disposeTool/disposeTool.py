from binary_reader import BinaryReader, Endian
import sys
import json

def read_file(filename):
    with open(filename, 'rb') as file:
        dp = BinaryReader(file.read(), Endian.BIG, encoding="shift-jis")
    data = dict()
    str_count = dp.read_uint16()
    dp.seek(2,1)
    str_tbl_ptr = dp.read_uint32()
    with dp.seek_to(str_tbl_ptr):
        for i in range(str_count):
            data[i] = dict()
            with dp.seek_to(dp.read_uint32()):
                data[i]["Original"] = dp.read_str()
                data[i]["New"] = ""

    with open(f'{filename}.json', 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def rebuild(input_file):
    with open(input_file, encoding='UTF-8') as f:
        data = json.loads(f.read())

    # header
    head = BinaryReader(endianness=Endian.BIG, encoding="shift-jis")
    head.write_uint16(len(data))
    head.write_uint16(0)
    head.write_uint32(head.pos() + 4)
    str_tbl_br = BinaryReader(endianness=Endian.BIG, encoding="shift-jis")
    str_br = BinaryReader(endianness=Endian.BIG, encoding="shift-jis")
    str_tbl_size = 4 * len(data)
    for i in range(len(data)):
        str_tbl_br.write_uint32(str_br.pos() + str_tbl_size + head.size())

        if len(data[str(i)]["New"]) == 0:
            string_to_write = data[str(i)]["Original"]
        else:
            string_to_write = data[str(i)]["New"]

        str_br.write_str(string_to_write, null=True)
    head.extend(str_tbl_br.buffer())
    head.seek(0, 2)
    head.extend(str_br.buffer()) 
    with open(f'{input_file}.bin', 'wb') as f:
        f.write(head.buffer())

def main():
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
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')

if __name__ == "__main__":
    main()
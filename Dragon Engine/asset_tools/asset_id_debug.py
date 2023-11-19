from binary_reader import BinaryReader
import sys
import json

def read_file(ass):
    data = dict()
    data['Magic'] = ass.read_str(4)
    data['Endian check'] = ass.read_uint32()
    data['Version'] = ass.read_uint32()
    ass.seek(4, 1)  # empty
    data['Asset count'] = ass.read_uint32()
    assets_list = list()
    for i in range(data['Asset count']):
        asset = dict()
        asset['ID'] = i
        pointer = ass.read_uint32()
        if pointer != 0:
            prev_pos = ass.pos()
            ass.seek(pointer)
            asset['Text'] = ass.read_str()
            ass.seek(prev_pos)
        assets_list.append(asset)
    data['Assets'] = assets_list

    return data

def main():
    if len(sys.argv) > 1:
        input_files = sys.argv[1:]
        file_count = 0
        for file in input_files:
            with open(file, 'rb') as f:
                data =  read_file(BinaryReader(f.read()))
            with open(f'{file}.json', 'w', encoding='UTF-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            file_count += 1

        print(f'{file_count} file(s) rebuilt.')
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')


if __name__ == "__main__":
    main()
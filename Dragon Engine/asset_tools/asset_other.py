from binary_reader import BinaryReader
import sys
import json

def read_file(ass):
    data = dict()
    data['Magic'] = ass.read_str(4)
    data['Endian check'] = ass.read_uint32()
    data['Version'] = ass.read_uint32()
    ass.seek(4, 1)  # empty
    data['Asset count'] = (ass.read_uint32() - 16) // 4
    ass.seek(-4, 1)
    assets_list = list()
    for i in range(data['Asset count']):
        asset = dict()
        asset['ID'] = i
        asset['Pointer'] = ass.read_uint32()
        assets_list.append(asset)

    for i in range(len(assets_list)):
        asset = assets_list[i]
        if i != len(assets_list) - 1:
            asset['End pointer'] = assets_list[i+1]['Pointer']
        else:
            asset['End pointer'] = ass.size()
        asset['Size'] = asset['End pointer'] - asset['Pointer']
        data_list = list()
        for i in range(asset['Size'] // 4):
            data_list.append(ass.read_uint32())
        asset['Data'] = data_list

    data['Assets'] = assets_list
    return data

def rebuild(data):

    # header
    head = BinaryReader()
    head.write_str(data['Magic'])
    head.write_uint32(33)  # endian check
    head.write_uint32(data['Version'])
    head.write_uint32(0)  # Padding
    main_header_size = head.size() + (len(data['Assets']) * 4)
    sub = BinaryReader()  # sub header
    for sub_data in data['Assets']:
        ass = BinaryReader()  # main data
        head.write_uint32(main_header_size + sub.size())
        for data in sub_data['Data']:
            ass.write_uint32(data)
        sub.extend(ass.buffer())
        sub.seek(ass.size(), 1)
    head.extend(sub.buffer())
    return head.buffer()

def main():
    if len(sys.argv) > 1:
        input_files = sys.argv[1:]
        file_count = 0
        for file in input_files:
            if file.endswith(".json"):
                with open(file, encoding='UTF-8') as f:
                    data = rebuild(json.loads(f.read()))
                with open(f'{file}.dat', 'wb') as f:
                    f.write(data)
            else:
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
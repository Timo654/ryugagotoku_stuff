import sys
import json
from binary_reader import BinaryReader    

def get_checksum(char_name):
    i = 0
    checksum = 0
    while i < len(char_name):
        value = ord(char_name[i])
        checksum += value
        i += 1
    return checksum

def import_to_bin(input_file, output_file):
    with open(input_file) as f:
        data = json.loads(f.read())
    info = BinaryReader(bytearray(), True)


    # HEADER
    info.write_uint32(0)
    info.write_uint16(0x201) #endian check
    info.write_uint32(0)
    info.write_uint32(0)
    info.write_uint16(0)
    info.write_uint32(len(data['Items']))
    info.write_uint32(len(data['Models']))
    info.write_uint32(0)
    info.write_uint32(0)

    # NOTES
    i = 0
    while i < len(data['Items']):
        item = data['Items'][i]
        info.write_uint16(i) #ID
        info.write_uint16(item['Face model'])
        info.write_uint16(item['Bottom model'])

        info.write_uint32(0)
        info.write_uint32(0)
        info.write_uint16(0)

        info.write_uint8(item['Unk3'])
        info.write_uint8(item['Unk4'])
        info.write_uint8(item['Unk5'])
        info.write_uint8(item['Unk6'])
        info.write_uint8(item['Unk7'])
        info.write_uint8(item['Unk8'])
        info.write_uint8(item['Unk9'])
        info.write_uint8(item['Unk10'])
        info.write_uint8(item['Unk11'])
        info.write_uint8(item['Unk12'])
        info.write_uint8(item['Unk13'])
        info.write_uint8(item['Unk14'])
        info.write_uint8(item['Unk15'])
        info.write_uint8(item['Unk16'])
        info.write_uint8(item['Unk17'])
        info.write_uint8(item['Unk18'])

        i += 1

    i = 0
    while i < len(data['Models']):
        model = data['Models'][i]
        info.write_uint16(get_checksum(model['Model name']))
        info.write_str(model['Model name'])
        info.align(0x20)
        i += 1


    with open(output_file, 'wb') as f:
        f.write(info.buffer())


def write_file(input_file):
    output_file = f'{input_file}.bin'
    import_to_bin(input_file, output_file)

def export_to_json(input_file, output_file):
    file = open(input_file, 'rb')
    info = BinaryReader(file.read(), True)
    file.close()

    data = {}
    # HEADER
    data['Header'] = {}
    info.seek(4, 1)
    data['Header']['Endian check'] = hex(info.read_uint16())
    info.seek(10, 1)
    data['Header']['Item Count'] = info.read_uint32()
    data['Header']['Model count'] = info.read_uint32()
    info.seek(8, 1)

    # NOTES
    item_list = []
    i = 0
    while i < data['Header']['Item Count']:
        item = {}
        item['Index'] = i
        item['Position'] = info.pos()
        item['ID'] = info.read_uint16()
        item['Face model'] = info.read_uint16()
        item['Bottom model'] = info.read_uint16()
        info.seek(10, 1)

        item['Unk3'] = info.read_uint8()
        item['Unk4'] = info.read_uint8()
        item['Unk5'] = info.read_uint8()
        item['Unk6'] = info.read_uint8()
        item['Unk7'] = info.read_uint8()
        item['Unk8'] = info.read_uint8()
        item['Unk9'] = info.read_uint8()
        item['Unk10'] = info.read_uint8()
        item['Unk11'] = info.read_uint8()
        item['Unk12'] = info.read_uint8()
        item['Unk13'] = info.read_uint8()
        item['Unk14'] = info.read_uint8()
        item['Unk15'] = info.read_uint8()
        item['Unk16'] = info.read_uint8()
        item['Unk17'] = info.read_uint8()
        item['Unk18'] = info.read_uint8()

        item_list.append(item)
        i += 1
    data['Items'] = item_list

    i = 0
    model_list = []
    while i < data['Header']['Model count']:
        model = {}
        model['Index'] = i
        info.seek(2, 1) #checksum
        model['Model name'] = info.read_str(0x1E)
        model_list.append(model)
        i += 1

    data['Models'] = model_list

    with open(output_file, 'w') as fp:
        json.dump(data, fp, indent=2)


def read_file(input_file):
    output_file = f'{input_file}.json'
    export_to_json(input_file, output_file)


def main():
    if len(sys.argv) > 1:
        input_files = sys.argv[:1]
        file_count = 0
        for file in input_files:
            if file.endswith(".json"):
                write_file(file)
            else:
                read_file(file)
            file_count += 1

        print(f'{file_count} file(s) rebuilt.')
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')


if __name__ == "__main__":
    main()

import argparse
import json
import os
from binary_reader import BinaryReader    

def export_to_json(input_file, output_file):
    file = open(input_file, 'rb')
    nl = BinaryReader(file.read(), True)
    file.close()

    data = {}
    # HEADER
    data['Header'] = {}
    nl.seek(4, 1)
    data['Header']['Endian check'] = hex(nl.read_uint16())
    nl.seek(10, 1)
    data['Header']['Character count'] = nl.read_uint32()
    nl.seek(0x2C, 1)

    # NOTES
    i = 0
    model_list = []
    while i < data['Header']['Character count'] - 1:
        print(i)
        model = {}
        model['Index'] = i
        print(nl.pos())
        nl.seek(2, 1) #checksum
        model['Model name'] = nl.read_str(0x1E)
        model_list.append(model)
        i += 1

    data['Characters'] = model_list

    with open(output_file, 'w') as fp:
        json.dump(data, fp, indent=2)


def load_file(input_file):
    output_file = f'{input_file}.json'
    export_to_json(input_file, output_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input",  help='Input file (.bin)',
                        type=str, nargs='+')
    args = parser.parse_args()

    input_files = args.input
    file_count = 0
    for file in input_files:
        load_file(file)
        file_count += 1
    print(f'{file_count} file(s) converted.')
    os.system('pause')


if __name__ == "__main__":
    main()

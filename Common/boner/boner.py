# yakuza bone copy thingy, ver 1.1
# thanks to Kan for the method and testing, TGE for GMD 010 editor template, Sutando for PyBinaryReader
# and metman for ruining my day
from binary_reader import BinaryReader, Endian
import argparse


def read_swap_list(file):
    with open(file, 'r') as f:
        data = f.readlines()
    swap_list = list()
    for name in data:
        name = name.strip()
        if not name.startswith(';'):  # comment
            swap_list.append(name)
    return swap_list


def read_gmd(gmd):
    data = dict()
    magic = gmd.read_str(4)
    if magic != 'GSGM':
        raise ValueError('Invalid magic, not a valid GMD file!')
    gmd.seek(1, 1)
    endian_check = gmd.read_uint8()
    if endian_check == 1:
        gmd.set_endian(Endian.BIG)
    gmd.seek(48)
    data['Node Pointer'] = gmd.read_uint32()
    gmd.seek(36, 1)
    data['Bone Matrice Pointer'] = gmd.read_uint32()
    data['Bone Count'] = gmd.read_uint32()
    gmd.seek(32, 1)
    string_pointer = gmd.read_uint32()
    string_count = gmd.read_uint32()
    gmd.seek(string_pointer)
    data['Strings'] = list()
    for _ in range(string_count):
        gmd.seek(2, 1)  # checksum
        data['Strings'].append(gmd.read_str(30, encoding="shift-jis"))

    return data


def read_strings(gmd, string_count, string_pointer):
    gmd.seek(string_pointer)
    strings = list()
    for _ in range(string_count):
        gmd.seek(2, 1)  # checksum
        strings.append(gmd.read_str(30, encoding="shift-jis"))
    return strings


def write_bone_info(fixed_model, data, swap_list):
    with open(fixed_model, 'rb') as file:
        gmd = BinaryReader(file.read())
    fixed_data = read_gmd(gmd)
    gmd.seek(data['Node Pointer'])

    for i in range(fixed_data['Bone Count']):
        gmd.seek(24, 1)
        bone_id = gmd.read_uint32()
        name = fixed_data['Strings'][bone_id]
        if name in data['Bones'] and name.startswith(tuple(swap_list)):
            print('Replaced', name)
            gmd.write_float(data['Bones'][fixed_data['Strings'][bone_id]][1])
            prev_pos = gmd.pos()
            matrice_pointer = fixed_data['Bone Matrice Pointer'] + i * 64
            gmd.seek(matrice_pointer)
            gmd.write_float(data['Bones'][fixed_data['Strings'][bone_id]][0])
            gmd.seek(prev_pos)
        else:
            gmd.seek(100, 1)
    with open(f'{fixed_model}_new.gmd', 'wb') as f:
        f.write(gmd.buffer())


def get_bone_info(original_model):
    with open(original_model, 'rb') as file:
        gmd = BinaryReader(file.read())
    data = read_gmd(gmd)

    gmd.seek(data['Bone Matrice Pointer'])
    bone_matrices = list()
    for _ in range(data['Bone Count']):
        bone_matrices.append(gmd.read_float(16))

    data['Bones'] = dict()
    gmd.seek(data['Node Pointer'])
    for i in range(data['Bone Count']):
        gmd.seek(24, 1)
        bone_id = gmd.read_uint32()
        data['Bones'][data['Strings'][bone_id]] = list()
        data['Bones'][data['Strings'][bone_id]].append(bone_matrices[i])
        data['Bones'][data['Strings'][bone_id]].append(gmd.read_float(25))

    return data


def read_file(fixed_model, source_model, swap_list):
    data = get_bone_info(source_model)
    swap_list = read_swap_list(swap_list)
    write_bone_info(fixed_model, data, swap_list)


def main():
    parser = argparse.ArgumentParser(description='Yakuza bone copier')
    parser.add_argument('-i', '--input', nargs="+",
                        help='Model(s) to copy bones to', required=True)
    parser.add_argument(
        '-s', '--source', help='Model to copy bones from', required=True)
    parser.add_argument(
        '-l', '--list', help='Text file with list of bones to copy', default='swap_list.txt')
    args = parser.parse_args()
    file_count = 0
    for file in args.input:
        read_file(file, args.source, args.list)
        file_count += 1

    print(f'{file_count} file(s) exported.')


if __name__ == "__main__":
    main()

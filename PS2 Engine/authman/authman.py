import json
from binary_reader import BinaryReader, Whence
import sys
import os


def extract_file(br, filename, size, output):
    out_name = os.path.join(output, filename)
    with open(out_name, "wb") as f:
        f.write(br.buffer()[br.pos():br.pos()+size])


def read_file(filename):
    output = os.path.join(os.path.dirname(filename), os.path.splitext(
        os.path.basename(filename))[0] + "_unpack")
    with open(filename, 'rb') as file:
        ass = BinaryReader(file.read())
    data = dict()
    ome_start_ptr = ass.read_uint32()
    ome_cnt = ass.read_uint32()
    txb_start_ptr = ass.read_uint32()
    txb_cnt = ass.read_uint32()
    misc_start_ptr = ass.read_uint32()
    misc_cnt = ass.read_uint32()
    data["FileType"] = "PS2Cutscene"  # so i can easily detect in noesis
    data['Field18'] = ass.read_uint32()
    data['Field1C'] = ass.read_uint32()

    os.makedirs(output, exist_ok=True)
    data["Models"] = dict()
    data["Textures"] = dict()
    data["Misc"] = dict()
    if ome_cnt != 0:
        ass.seek(ome_start_ptr)
        for ome in range(ome_cnt):
            node = dict()
            size = ass.read_uint32()
            node["Unk"] = ass.read_uint32()
            node["Unk2"] = ass.read_uint32()
            node["Unk3"] = ass.read_uint32()
            filename = f'{ome}.OME'
            extract_file(ass, filename, size, output)
            ass.seek(size, Whence.CUR)
            data["Models"][filename] = node
    if txb_cnt != 0:
        ass.seek(txb_start_ptr)
        for txb in range(txb_cnt):
            node = dict()
            size = ass.read_uint32()
            node["Unk"] = ass.read_uint32()
            node["Unk2"] = ass.read_uint32()
            node["Unk3"] = ass.read_uint32()
            filename = f'{txb}.TXB'
            extract_file(ass, filename, size, output)
            ass.seek(size, Whence.CUR)
            data["Textures"][filename] = node
    if misc_cnt != 0:
        ass.seek(misc_start_ptr)
        for misc in range(misc_cnt):
            node = dict()
            size = ass.read_uint32()
            node["Type"] = ass.read_uint32()
            if node["Type"] in [0, 5, 6]:
                filename = f'{misc}.SGT'
            elif node["Type"] == 2:
                filename = f'{misc}.SUB'
            else:
                filename = f'{misc}.DAT'

            node["Unk2"] = ass.read_uint32()
            node["Unk3"] = ass.read_uint32()
            extract_file(ass, filename, size, output)
            ass.seek(size, Whence.CUR)
            data["Misc"][filename] = node

    with open(os.path.join(output, 'manifest.json'), 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=2)


def rebuild(input_folder):
    with open(os.path.join(input_folder, "manifest.json"), encoding='UTF-8') as f:
        data = json.loads(f.read())
    # header
    head = BinaryReader()
    body = BinaryReader()
    head.write_uint32(64)  # header is always 32 bytes
    head.write_uint32(len(data["Models"]))
    for model in data["Models"]:
        with open(os.path.join(input_folder, model), "rb") as f:
            file = BinaryReader(f.read())
        body.write_uint32(file.size())
        body.write_uint32(0)
        # no clue what this is, but it's been used for OME everywhere
        body.write_uint32(1431194446)
        body.write_uint32(0)
        body.extend(file.buffer())
        body.seek(0, Whence.END)

    head.write_uint32(body.size() + 64)
    head.write_uint32(len(data["Textures"]))
    for texture in data["Textures"]:
        with open(os.path.join(input_folder, texture), "rb") as f:
            file = BinaryReader(f.read())
        body.write_uint32(file.size())
        body.write_uint32(data["Textures"][texture]["Unk"])
        body.write_uint32(data["Textures"][texture]["Unk2"])
        body.write_uint32(data["Textures"][texture]["Unk3"])
        body.extend(file.buffer())
        body.seek(0, Whence.END)

    head.write_uint32(body.size() + 64)
    head.write_uint32(len(data["Misc"]))
    for misc in data["Misc"]:
        with open(os.path.join(input_folder, misc), "rb") as f:
            file = BinaryReader(f.read())
        body.write_uint32(file.size())
        body.write_uint32(data["Misc"][misc]["Type"])
        body.write_uint32(data["Misc"][misc]["Unk2"])
        body.write_uint32(data["Misc"][misc]["Unk3"])
        body.extend(file.buffer())
        body.seek(0, Whence.END)

    head.write_uint32(data["Field18"])
    head.write_uint32(data["Field1C"])
    head.pad(0x20)
    head.extend(body.buffer())

    output_name = f'{input_folder}.dat'.replace("_unpack", "")
    with open(output_name, 'wb') as f:
        f.write(head.buffer())


def main():
    if len(sys.argv) > 1:
        input_files = sys.argv[1:]
        file_count = 0
        for file in input_files:
            if not file.endswith("dat"):
                continue
            if os.path.isdir(file):
                rebuild(file)
            else:
                read_file(file)
            file_count += 1
        print(f'{file_count} file(s) rebuilt.')
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')


if __name__ == "__main__":
    main()

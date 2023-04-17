from binary_reader import BinaryReader
import os
import pandas as pd

dir_name = input("Enter sound directory path: ")

def get_list_of_files(dir_name):
    all_files = list()
    for (root, _, files) in os.walk(dir_name):
        for f in files:
            all_files.append(os.path.join(root, f))

    return all_files

def do_stuff(input_file):
    file = open(input_file, 'rb')
    acb = BinaryReader(file.read(), True)
    file.close()
    acb.seek(8, 1)
    header_end_pos = acb.pos()
    acb.seek(2, 1)
    rows_pos = acb.read_uint16()
    text_pos = acb.read_uint32()
    acb.seek(header_end_pos)
    acb.seek(rows_pos, 1)
    acb.seek(219, 1)
    name_pos = acb.read_uint32()
    acb.seek(header_end_pos)
    acb.seek(text_pos, 1)
    acb.seek(name_pos, 1)
    name = acb.read_str()
    return name

file_list = get_list_of_files(dir_name)

name_list = []
file_dec_list = []
file_hex_list = []
df = pd.DataFrame()
i = 0
for i in range(len(file_list)):
    if file_list[i].endswith('.acb'):
        name = do_stuff(file_list[i])

        file_hex_list.append((os.path.basename(file_list[i])[:4]))
        file_dec_list.append(int(os.path.basename(file_list[i])[:4], 16))
        if name == 'Header':
            name = 'None'
        name_list.append(name)

df['Cuesheet ID (Decimal)'] = file_dec_list
df['Cuesheet ID (Hex)'] = file_hex_list
df['Name'] = name_list
df.to_excel('acb_list.xlsx', index=False)
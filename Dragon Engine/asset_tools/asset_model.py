from binary_reader import BinaryReader
import sys
import json

def write_model_info_flag(data):
    flag = 0
    if data['is_have_normal']: flag |= 0x1
    if data['is_have_break1']: flag |= 0x2
    if data['is_have_break2']: flag |= 0x4
    if data['is_have_scrap1']: flag |= 0x8
    if data['is_have_scrap2']: flag |= 0x10
    if data['is_have_scrape']: flag |= 0x20
    if data['dummy6']: flag |= 0x40
    if data['dummy7']: flag |= 0x80
    if data['dummy8']: flag |= 0x100
    if data['dummy9']: flag |= 0x200
    if data['dummy10']: flag |= 0x400
    if data['dummy11']: flag |= 0x800
    if data['is_have_normal_l0']: flag |= 0x1000
    if data['is_have_normal_l1']: flag |= 0x2000
    if data['is_have_normal_l2']: flag |= 0x4000
    if data['is_have_break1_l0']: flag |= 0x8000
    if data['is_have_break1_l1']: flag |= 0x10000
    if data['is_have_break1_l2']: flag |= 0x20000
    if data['is_have_break2_l0']: flag |= 0x40000
    if data['is_have_break2_l1']: flag |= 0x80000
    if data['is_have_break2_l2']: flag |= 0x100000
    if data['dummy21']: flag |= 0x200000
    if data['dummy22']: flag |= 0x400000
    if data['dummy23']: flag |= 0x800000
    if data['is_have_render_texture']: flag |= 0x1000000
    if data['dummy24_31']: flag |= 0x2000000
    return flag

def rebuild(data):
    # header
    head = BinaryReader()
    head.write_str('AMLB')
    head.write_uint32(33)  # endian check
    head.write_uint32(data['Version'])
    head.write_uint32(0)  # Padding
    head.write_uint32(len(data['Assets']))
    main_header_size = head.size() + (len(data['Assets']) * 4)
    sub_header_size = 256  # 64 * 4
    sub = BinaryReader()  # sub header
    for i in range(len(data['Assets'])):
        ass = BinaryReader()  # main data
        head.write_uint32(main_header_size + sub.size())
        sub_data = data['Assets'][i]
        for o in range(64):
            if o < len(sub_data['Data']):
                sub.write_uint32(sub_header_size + ass.size())
                asset_data = sub_data['Data'][o]
                ass.write_uint32(asset_data['Version'])
                if o == 0:
                    ass.write_str_fixed(asset_data['Name'], size=32)
                elif o == 1:
                    ass.write_float(asset_data['orbox_normal_cx'])
                    ass.write_float(asset_data['orbox_normal_cy'])
                    ass.write_float(asset_data['orbox_normal_cz'])
                    ass.write_float(asset_data['orbox_normal_ex'])
                    ass.write_float(asset_data['orbox_normal_ey'])
                    ass.write_float(asset_data['orbox_normal_ez'])
                    ass.write_float(asset_data['orbox_break1_cx'])
                    ass.write_float(asset_data['orbox_break1_cy'])
                    ass.write_float(asset_data['orbox_break1_cz'])
                    ass.write_float(asset_data['orbox_break1_ex'])
                    ass.write_float(asset_data['orbox_break1_ey'])
                    ass.write_float(asset_data['orbox_break1_ez'])
                    ass.write_float(asset_data['orbox_break2_cx'])
                    ass.write_float(asset_data['orbox_break2_cy'])
                    ass.write_float(asset_data['orbox_break2_cz'])
                    ass.write_float(asset_data['orbox_break2_ex'])
                    ass.write_float(asset_data['orbox_break2_ey'])
                    ass.write_float(asset_data['orbox_break2_ez'])
                elif o == 2:
                    ass.write_uint32(write_model_info_flag(asset_data['Flags']))
                    ass.write_int32(asset_data['scrap_start_idx'])
                    ass.write_uint64(0)  # padding
                    ass.write_uint64(0)  # padding
                    ass.write_uint64(0)  # padding
                elif o == 3:
                    if 'Node Pos Type' in asset_data:
                        ass.write_uint32(
                            len(asset_data['Node Pos Type']))  # item count
                        for o in range(len(asset_data['Node Pos Type'])):
                            node_pos_type = asset_data['Node Pos Type'][o]
                            ass.write_uint32(node_pos_type['e_id'])
                            ass.write_uint32(node_pos_type['node_id'])
                    else:
                        ass.write_uint32(0)

                elif o == 4:
                    if 'Cloth table' in asset_data:
                        ass.write_uint32(len(asset_data['Cloth table']))
                        ass.write_uint32(asset_data['X num'])
                        ass.write_uint32(asset_data['Y num'])
                        ass.write_float(asset_data['Pos X'])
                        ass.write_float(asset_data['Pos Y'])
                        ass.write_float(asset_data['Pos Z'])
                        ass.write_float(asset_data['X length'])
                        ass.write_float(asset_data['Y length'])
                        for o in range(len(asset_data['Cloth table'])):
                            cloth_node = asset_data['Cloth table'][o]
                            ass.write_uint32(cloth_node['X index'])
                            ass.write_uint32(cloth_node['Y index'])
                            ass.write_uint32(cloth_node['Node ID'])
                            ass.write_uint8(cloth_node['is_effecter'])
                            ass.write_uint16(0)  # padding
                            ass.write_uint8(0)  # padding
                            ass.write_float(cloth_node['Effecter Pos X'])
                            ass.write_float(cloth_node['Effecter Pos Y'])
                            ass.write_float(cloth_node['Effecter Pos Z'])
                            ass.write_float(cloth_node['Effecter Pos W'])
                    else:
                        ass.write_uint32(0)  # no values
                elif o == 5:
                    ass.write_float(asset_data['lod_draw_factor_hm'])
                    ass.write_float(asset_data['lod_draw_factor_ml'])
                    ass.write_uint64(0)  # Padding
            else:
                sub.write_uint32(0)  # no pointer
        sub.extend(ass.buffer())
        sub.seek(ass.size(), 1)
    head.extend(sub.buffer())
    return head.buffer()

def read_model_info_flag(flag):
    data = dict()
    data['is_have_normal'] = bool(flag & 0x1)
    data['is_have_break1'] = bool(flag & 0x2)
    data['is_have_break2'] = bool(flag & 0x4)
    data['is_have_scrap1'] = bool(flag & 0x8)
    data['is_have_scrap2'] = bool(flag & 0x10)
    data['is_have_scrape'] = bool(flag & 0x20)
    data['dummy6'] = bool(flag & 0x40)
    data['dummy7'] = bool(flag & 0x80)
    data['dummy8'] = bool(flag & 0x100)
    data['dummy9'] = bool(flag & 0x200)
    data['dummy10'] = bool(flag & 0x400)
    data['dummy11'] = bool(flag & 0x800)
    data['is_have_normal_l0'] = bool(flag & 0x1000)
    data['is_have_normal_l1'] = bool(flag & 0x2000)
    data['is_have_normal_l2'] = bool(flag & 0x4000)
    data['is_have_break1_l0'] = bool(flag & 0x8000)
    data['is_have_break1_l1'] = bool(flag & 0x10000)
    data['is_have_break1_l2'] = bool(flag & 0x20000)
    data['is_have_break2_l0'] = bool(flag & 0x40000)
    data['is_have_break2_l1'] = bool(flag & 0x80000)
    data['is_have_break2_l2'] = bool(flag & 0x100000)
    data['dummy21'] = bool(flag & 0x200000)
    data['dummy22'] = bool(flag & 0x400000)
    data['dummy23'] = bool(flag & 0x800000)
    data['is_have_render_texture'] = bool(flag & 0x1000000)
    data['dummy24_31'] = bool(flag & 0x2000000)
    return data

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
            data_list = list()
            for o in range(64):  # offset_tbl_t
                asset_data = dict()
                asset_data['Index'] = o
                pointer2 = ass.read_uint32()
                if pointer2 != 0:
                    prev_pos2 = ass.pos()
                    ass.seek(pointer + pointer2)
                    asset_data['Version'] = ass.read_uint32()
                    if o == 0:
                        asset_data['Name'] = ass.read_str(32)
                    elif o == 1:
                        asset_data['orbox_normal_cx'] = ass.read_float()
                        asset_data['orbox_normal_cy'] = ass.read_float()
                        asset_data['orbox_normal_cz'] = ass.read_float()
                        asset_data['orbox_normal_ex'] = ass.read_float()
                        asset_data['orbox_normal_ey'] = ass.read_float()
                        asset_data['orbox_normal_ez'] = ass.read_float()
                        asset_data['orbox_break1_cx'] = ass.read_float()
                        asset_data['orbox_break1_cy'] = ass.read_float()
                        asset_data['orbox_break1_cz'] = ass.read_float()
                        asset_data['orbox_break1_ex'] = ass.read_float()
                        asset_data['orbox_break1_ey'] = ass.read_float()
                        asset_data['orbox_break1_ez'] = ass.read_float()
                        asset_data['orbox_break2_cx'] = ass.read_float()
                        asset_data['orbox_break2_cy'] = ass.read_float()
                        asset_data['orbox_break2_cz'] = ass.read_float()
                        asset_data['orbox_break2_ex'] = ass.read_float()
                        asset_data['orbox_break2_ey'] = ass.read_float()
                        asset_data['orbox_break2_ez'] = ass.read_float()
                    elif o == 2:
                        asset_data['Flags'] = read_model_info_flag(ass.read_uint32())
                        asset_data['scrap_start_idx'] = ass.read_int32()
                        ass.seek(24, 1)  # padding
                    elif o == 3:
                        asset_data['ItemCount'] = ass.read_uint32()
                        node_pos_list = list()
                        if asset_data['ItemCount'] != 0:
                            for o in range(asset_data['ItemCount']):
                                node_pos_type = dict()
                                node_pos_type['e_id'] = ass.read_uint32()
                                node_pos_type['node_id'] = ass.read_uint32()
                                node_pos_list.append(node_pos_type)
                            asset_data['Node Pos Type'] = node_pos_list
                    elif o == 4:
                        asset_data['Node count'] = ass.read_uint32()
                        if asset_data['Node count'] != 0:
                            asset_data['X num'] = ass.read_uint32()
                            asset_data['Y num'] = ass.read_uint32()
                            asset_data['Pos X'] = ass.read_float()
                            asset_data['Pos Y'] = ass.read_float()
                            asset_data['Pos Z'] = ass.read_float()
                            asset_data['X length'] = ass.read_float()
                            asset_data['Y length'] = ass.read_float()
                            cloth_list = list()
                            for o in range(asset_data['Node count']):
                                cloth_node = dict()
                                cloth_node['X index'] = ass.read_uint32()
                                cloth_node['Y index'] = ass.read_uint32()
                                cloth_node['Node ID'] = ass.read_uint32()
                                cloth_node['is_effecter'] = ass.read_uint8()
                                ass.seek(3, 1)  # padding
                                cloth_node['Effecter Pos X'] = ass.read_float()
                                cloth_node['Effecter Pos Y'] = ass.read_float()
                                cloth_node['Effecter Pos Z'] = ass.read_float()
                                cloth_node['Effecter Pos W'] = ass.read_float()
                                cloth_list.append(cloth_node)
                            asset_data['Cloth table'] = cloth_list
                    elif o == 5:  # added in judgment
                        asset_data['lod_draw_factor_hm'] = ass.read_float()
                        asset_data['lod_draw_factor_ml'] = ass.read_float()
                        ass.seek(8, 1)  # padding
                    ass.seek(prev_pos2)
                    data_list.append(asset_data)
            asset['Data'] = data_list
            ass.seek(prev_pos)
        assets_list.append(asset)
    data['Assets'] = assets_list

    return data

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
                    json.dump(data, f, indent=2)
            file_count += 1

        print(f'{file_count} file(s) rebuilt.')
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')


if __name__ == "__main__":
    main()
from binary_reader import BinaryReader
import sys
import json

def read_asset_id_flag(flag):
    data = dict()
    data['break_blast'] = bool(flag & 0x1)
    data['only_blast_break'] = bool(flag & 0x2)
    data['is_burning'] = bool(flag & 0x4)
    data['disable_blast_break'] = bool(flag & 0x8)
    data['is_no_owner_break'] = bool(flag & 0x10)
    data['is_project_disable'] = bool(flag & 0x20)
    data['dummy'] = bool(flag & 0x40)
    return data

def read_modeltype_flag(flag):
    data = dict()
    data['is_tree_model'] = bool(flag & 0x1)
    data['dummy'] = bool(flag & 0x2)
    return data

def read_type_flag(flag):
    data = dict()
    data['is_move_limit'] = bool(flag & 0x1)
    data['is_inclination_limit'] = bool(flag & 0x2)
    data['is_obstacle_auto'] = bool(flag & 0x4)
    data['is_obstacle_is'] = bool(flag & 0x8)
    data['is_obstacle_navi'] = bool(flag & 0x10)
    data['is_have_break'] = bool(flag & 0x20)
    data['is_move_limit_disable'] = bool(flag & 0x40)
    data['is_physics_ignore_mass_min_limit'] = bool(flag & 0x80)
    data['is_fixed_physics_with_sight_ct'] = bool(flag & 0x100)
    data['is_obstacle_sight_not_through'] = bool(flag & 0x200)
    data['is_drone_disable_sheded'] = bool(flag & 0x400)
    data['is_fixed_physics_with_camera_ct'] = bool(flag & 0x800)
    data['is_door_off_sight_filter'] = bool(flag & 0x1000)
    data['is_door_on_occlusion'] = bool(flag & 0x2000)
    data['is_break_kanban'] = bool(flag & 0x4000)
    data['dummy'] = bool(flag & 0x8000)
    return data

def read_presettype_flag(flag):
    data = dict()
    data['is_parent_break_sametime'] = bool(flag & 0x1)
    data['dummy'] = bool(flag & 0x2)
    return data

def read_display_flag(flag):
    data = dict()
    data['is_uv_offset'] = bool(flag & 0x1)
    data['is_nearclip_scale_use'] = bool(flag & 0x2)
    data['is_shadow_disable'] = bool(flag & 0x4)
    data['dummy3'] = bool(flag & 0x8)
    data['is_node_culling'] = bool(flag & 0x10)
    data['is_color_change1'] = bool(flag & 0x20)
    data['is_color_change2'] = bool(flag & 0x40)
    data['is_cloth_wind_disable'] = bool(flag & 0x80)
    data['is_shadow_occlusion_unreceive'] = bool(flag & 0x100)
    data['is_shadow_far_visible'] = bool(flag & 0x200)
    data['is_nearclip_disable'] = bool(flag & 0x400)
    data['is_shadow_occlusion_visible'] = bool(flag & 0x800)
    data['is_resident_stage_movie'] = bool(flag & 0x1000)
    data['is_stage_enable_nearclip'] = bool(flag & 0x2000)
    data['is_force_invisible_mesh'] = bool(flag & 0x4000)
    data['is_highlight_always'] = bool(flag & 0x8000)
    data['is_texture_auto_lod_cv'] = bool(flag & 0x10000)
    data['dummy'] = bool(flag & 0x20000)
    return data

def read_anim_flag(flag):
    data = dict()
    data['is_reverse'] = bool(flag & 0x1)
    data['is_limitrot'] = bool(flag & 0x2)
    data['dummy'] = bool(flag & 0x4)
    return data

def read_attr_flag(flag):
    data = dict()
    data['electric_shock'] = bool(flag & 0x1)
    data['eye_blind'] = bool(flag & 0x2)
    data['stun'] = bool(flag & 0x4)
    data['flame'] = bool(flag & 0x8)
    data['slash'] = bool(flag & 0x10)
    data['cough'] = bool(flag & 0x20)
    data['dummy'] = bool(flag & 0x40)
    return data

def read_arms_flag(flag):
    data = dict()
    data['infinite_arms'] = bool(flag & 0x1)
    data['player_cant_pickup'] = bool(flag & 0x2)
    data['equip_fill_light'] = bool(flag & 0x4)
    data['throw_fly_straight'] = bool(flag & 0x8)
    data['dummy'] = bool(flag & 0x10)
    return data

def read_particle_flag(flag):
    data = dict()
    data['is_come_with'] = bool(flag & 0x1)
    data['is_shiny'] = bool(flag & 0x2)
    data['is_break_after_fade'] = bool(flag & 0x4)
    data['dummy'] = bool(flag & 0x8)
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
                        asset_data['PUID ID'] = ass.read_uint32()
                        asset_data['Name'] = ass.read_str(16)
                        asset_data['Broken asset PUID ID'] = ass.read_uint32()
                        asset_data['Prog ID'] = ass.read_uint32()
                        asset_data['Prog Sub ID'] = ass.read_uint32()
                        asset_data['Arms Category'] = ass.read_uint8()
                        asset_data['Arms Category Sub'] = ass.read_uint8()
                        asset_data['Hand pattern'] = ass.read_uint8()
                        asset_data['Use count'] = ass.read_int8()
                        asset_data['Durability'] = ass.read_uint8()
                        asset_data['Break blast param'] = ass.read_uint8()
                        asset_data['Durability Restraints Category'] = ass.read_uint8()
                        ass.seek(1, 1)  # padding
                        asset_data['Broken random asset PUID ID'] = ass.read_int32()
                        asset_data['Impact Power'] = ass.read_int32()
                        asset_data['Flags'] = read_asset_id_flag(ass.read_uint32())
                        asset_data['Pickup offset X'] = ass.read_float()
                        asset_data['Pickup offset Y'] = ass.read_float()
                        asset_data['Pickup offset Z'] = ass.read_float()
                        asset_data['Hact range'] = ass.read_uint32()
                        ass.seek(1, 1)  # padding
                    elif o == 1:
                        asset_data['Model ID'] = ass.read_uint32()
                        asset_data['Flags'] = read_modeltype_flag(ass.read_uint32())
                        asset_data['Geometry type'] = ass.read_uint8()
                        ass.seek(3, 1)  # Padding
                    elif o == 2:
                        asset_data['Replace texture num'] = ass.read_uint32()
                        ass.seek(8, 1)  # padding
                        if asset_data['Replace texture num'] != 0:
                            texture_list = list()
                            for i in range(asset_data['Replace texture num']):
                                tex = dict()
                                tex['Base texture'] = ass.read_str(32)
                                tex['Replacement texture'] = ass.read_str(32)
                                texture_list.append(tex)
                            asset_data['Texture replacement'] = texture_list
                    elif o == 3:
                        asset_data['Particle Count'] = ass.read_uint32()
                        ass.seek(8, 1)  # Padding
                        if asset_data['Particle Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Particle Count']):
                                item = dict()
                                item['Particle ID'] = ass.read_uint32()
                                ass.seek(1, 1)  # padding
                                item['Timing'] = ass.read_uint8()
                                item['Assign node'] = ass.read_uint8()
                                ass.seek(1, 1)  # padding
                                item['color_r'] = ass.read_uint8()
                                item['color_g'] = ass.read_uint8()
                                item['color_b'] = ass.read_uint8()
                                item['color_a'] = ass.read_uint8()
                                item['Flags'] = read_particle_flag(ass.read_uint32())
                                item['Shininess'] = ass.read_float()
                                item['ioe'] = ass.read_float()
                                ass.seek(8, 1)  # padding
                                item_list.append(item)
                            asset_data['Particle params'] = item_list
                    elif o == 4:
                        asset_data['Move mode'] = ass.read_uint8()
                        ass.seek(3, 1)  # Padding
                        asset_data['Flags'] = read_type_flag(ass.read_uint32())
                        asset_data['Move limit size'] = ass.read_float()
                        asset_data['Inclination limit param'] = ass.read_int32()
                        asset_data['Collision ID'] = ass.read_uint32()
                        ass.seek(8, 1)  # Padding
                    elif o == 5:  # used in LJ, may be incorrect
                        asset_data['Motion num'] = ass.read_uint32()
                        asset_data['Motion ID'] = ass.read_uint32()
                        if asset_data['Motion num'] != 0:
                            item_list = list()
                            for i in range(asset_data['Motion num']):
                                item = dict()
                                item['Unk1'] = ass.read_uint32()
                                item['Unk2'] = ass.read_uint32()
                                item_list.append(item)
                            asset_data['Motion list'] = item_list
                        asset_data['Unk3'] = ass.read_uint32()
                    elif o == 6:
                        asset_data['Preset Count'] = ass.read_uint32()
                        asset_data['Flags'] = read_presettype_flag(ass.read_uint32())
                        ass.seek(4, 1)  # Padding
                        if asset_data['Preset Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Preset Count']):
                                item = dict()
                                item['Asset ID'] = ass.read_uint32()
                                item['px'] = ass.read_float()
                                item['py'] = ass.read_float()
                                item['pz'] = ass.read_float()
                                item['ry'] = ass.read_float()
                                item['rx'] = ass.read_float()
                                item['rz'] = ass.read_float()
                                ass.seek(4, 1)  # Padding
                                item_list.append(item)
                            asset_data['Asset Presets'] = item_list
                    elif o == 7:
                        asset_data['Sound ID Category'] = ass.read_uint32()
                        ass.seek(24, 1)  # Padding
                    elif o == 8:
                        asset_data['Flags'] = read_display_flag(ass.read_uint32())
                        asset_data['UV offset U'] = ass.read_float()
                        asset_data['UV offset V'] = ass.read_float()
                        asset_data['Nearclip param'] = ass.read_float()
                        asset_data['Shadow occlusion luminance'] = ass.read_uint8()
                        ass.seek(3, 1)  # Padding
                        asset_data['Color change 1'] = ass.read_uint32()
                        asset_data['Color change 2'] = ass.read_uint32()
                        asset_data['Arm name'] = ass.read_uint32()
                        asset_data['Scrap fade time'] = ass.read_float()
                        asset_data['Effect highlight'] = ass.read_uint32()
                        asset_data['LOD Factor HM'] = ass.read_float()
                        asset_data['LOD Factor ML'] = ass.read_float()
                        asset_data['Scale'] = ass.read_float()
                        asset_data['Unk1'] = ass.read_float() # Added in LJ
                        asset_data['Unk2'] = ass.read_uint32() # Added in LJ
                    elif o == 9:
                        asset_data['Light Count'] = ass.read_uint32()
                        ass.seek(8, 1)  # Padding
                        if asset_data['Light Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Light Count']):
                                item = dict()
                                item['WGP_uid'] = ass.read_uint64()
                                ass.seek(1, 1)  # Padding
                                item['Timing'] = ass.read_uint8()
                                ass.seek(2, 1)  # Padding
                                item['Node ID'] = ass.read_uint32()
                                item_list.append(item)
                            asset_data['Lights'] = item_list
                    elif o == 10:
                        asset_data['Effect event Count'] = ass.read_uint32()
                        ass.seek(8, 1)  # Padding
                        if asset_data['Effect event Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Effect event Count']):
                                item = dict()
                                ass.seek(4, 1)  # Padding
                                item['Event ID'] = ass.read_uint32()
                                ass.seek(8, 1)  # Padding
                                item_list.append(item)
                            asset_data['Effect event params'] = item_list
                    elif o == 11:
                        asset_data['Animation Count'] = ass.read_uint32()
                        ass.seek(8, 1)  # Padding
                        if asset_data['Animation Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Animation Count']):
                                item = dict()
                                item['Node id'] = ass.read_uint32()
                                item['Axis'] = ass.read_uint32()
                                item['Speed'] = ass.read_float()
                                item['Flags'] = read_anim_flag(ass.read_uint32())
                                item['limitrot_l_dummy'] = ass.read_int32()
                                item['limitrot_r_dummy'] = ass.read_int32()
                                item['limitrot_l'] = ass.read_float()
                                item['limitrot_r'] = ass.read_float()
                                item_list.append(item)
                            asset_data['Animation params'] = item_list
                    elif o == 12:  # dummy_bullet, does not appear to be used in JE and up
                        asset_data['Item Count'] = ass.read_uint32()
                        ass.seek(8, 1)  # padding
                        if asset_data['Item Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Item Count']):
                                item = dict()
                                item['Unk1'] = ass.read_uint32()
                                item['Unk2'] = ass.read_uint32()
                                item['Unk3'] = ass.read_uint32()
                                item['Unk4'] = ass.read_uint32()
                                item_list.append(item)
                            asset_data['dummy_bullet params'] = item_list
                    elif o == 13:
                        asset_data['Arms padding'] = ass.read_uint32()
                        asset_data['Arms category'] = ass.read_uint8()
                        asset_data['Arms category sub'] = ass.read_uint8()
                        ass.seek(2, 1)  # Padding
                        asset_data['Attack scale'] = ass.read_float()
                        asset_data['Impact Param'] = ass.read_int32()
                        asset_data['Use count'] = ass.read_int32()
                        asset_data['Arm name'] = ass.read_uint32()
                        asset_data['Attributes'] = read_attr_flag(ass.read_uint32())
                        asset_data['Flags'] = read_arms_flag(ass.read_uint32())
                        asset_data['Infinite Arms ID'] = ass.read_uint32()
                        asset_data['Spray bomb'] = ass.read_uint32()
                        asset_data['Another handle arms'] = ass.read_uint32()
                        asset_data['Grenade Explode Time Player'] = ass.read_float()
                        asset_data['Grenade Explode Time Else'] = ass.read_float()
                        asset_data['Throw speed'] = ass.read_float()
                        asset_data['Arms Parameter'] = ass.read_uint32()
                        ass.seek(64, 1)  # Padding
                    elif o == 14: # added in judgment
                        asset_data['Replace language texture Count'] = ass.read_uint32()
                        ass.seek(8, 1)  # Padding
                        if asset_data['Replace language texture Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Replace language texture Count']):
                                item = dict()
                                item['Texture PUID index'] = ass.read_uint32()
                                ass.seek(12, 1)
                                item_list.append(item)
                            asset_data['Language texture replace list'] = item_list
                    elif o == 15: # added in lost judgment
                        asset_data['Unk Count'] = ass.read_uint32()
                        if asset_data['Unk Count'] != 0:
                            item_list = list()
                            for i in range(asset_data['Unk Count']):
                                item = dict()
                                item['Unk5'] = ass.read_uint32()
                                item_list.append(item)
                            asset_data['Unknown list'] = item_list
                    ass.seek(prev_pos2)
                    data_list.append(asset_data)
            asset['Data'] = data_list
            ass.seek(prev_pos)
        assets_list.append(asset)
    data['Assets'] = assets_list

    return data

def write_asset_id_flag(data):
    flag = 0
    if data['break_blast']: flag |= 0x1
    if data['only_blast_break']: flag |= 0x2
    if data['is_burning']: flag |= 0x4
    if data['disable_blast_break']: flag |= 0x8
    if data['is_no_owner_break']: flag |= 0x10
    if data['is_project_disable']: flag |= 0x20
    if data['dummy']: flag |= 0x40
    return flag

def write_modeltype_flag(data):
    flag = 0
    if data['is_tree_model']: flag |= 0x1
    if data['dummy']: flag |= 0x2
    return flag

def write_type_flag(data):
    flag = 0
    if data['is_move_limit']: flag |= 0x1
    if data['is_inclination_limit']: flag |= 0x2
    if data['is_obstacle_auto']: flag |= 0x4
    if data['is_obstacle_is']: flag |= 0x8
    if data['is_obstacle_navi']: flag |= 0x10
    if data['is_have_break']: flag |= 0x20
    if data['is_move_limit_disable']: flag |= 0x40
    if data['is_physics_ignore_mass_min_limit']: flag |= 0x80
    if data['is_fixed_physics_with_sight_ct']: flag |= 0x100
    if data['is_obstacle_sight_not_through']: flag |= 0x200
    if data['is_drone_disable_sheded']: flag |= 0x400
    if data['is_fixed_physics_with_camera_ct']: flag |= 0x800
    if data['is_door_off_sight_filter']: flag |= 0x1000
    if data['is_door_on_occlusion']: flag |= 0x2000
    if data['is_break_kanban']: flag |= 0x4000
    if data['dummy']: flag |= 0x8000
    return flag

def write_presettype_flag(data):
    flag = 0
    if data['is_parent_break_sametime']: flag |= 0x1
    if data['dummy']: flag |= 0x2
    return flag

def write_display_flag(data):
    flag = 0
    if data['is_uv_offset']: flag |= 0x1
    if data['is_nearclip_scale_use']: flag |= 0x2
    if data['is_shadow_disable']: flag |= 0x4
    if data['dummy3']: flag |= 0x8
    if data['is_node_culling']: flag |= 0x10
    if data['is_color_change1']: flag |= 0x20
    if data['is_color_change2']: flag |= 0x40
    if data['is_cloth_wind_disable']: flag |= 0x80
    if data['is_shadow_occlusion_unreceive']: flag |= 0x100
    if data['is_shadow_far_visible']: flag |= 0x200
    if data['is_nearclip_disable']: flag |= 0x400
    if data['is_shadow_occlusion_visible']: flag |= 0x800
    if data['is_resident_stage_movie']: flag |= 0x1000
    if data['is_stage_enable_nearclip']: flag |= 0x2000
    if data['is_force_invisible_mesh']: flag |= 0x4000
    if data['is_highlight_always']: flag |= 0x8000
    if data['is_texture_auto_lod_cv']: flag |= 0x10000
    if data['dummy']: flag |= 0x20000
    return flag

def write_anim_flag(data):
    flag = 0
    if data['is_reverse']: flag |= 0x1
    if data['is_limitrot']: flag |= 0x2
    if data['dummy']: flag |= 0x4
    return flag

def write_attr_flag(data):
    flag = 0
    if data['electric_shock']: flag |= 0x1
    if data['eye_blind']: flag |= 0x2
    if data['stun']: flag |= 0x4
    if data['flame']: flag |= 0x8
    if data['slash']: flag |= 0x10
    if data['cough']: flag |= 0x20
    if data['dummy']: flag |= 0x40
    return flag

def write_arms_flag(data):
    flag = 0
    if data['infinite_arms']: flag |= 0x1
    if data['player_cant_pickup']: flag |= 0x2
    if data['equip_fill_light']: flag |= 0x4
    if data['throw_fly_straight']: flag |= 0x8
    if data['dummy']: flag |= 0x10
    return flag

def write_particle_flag(data):
    flag = 0
    if data['is_come_with']: flag |= 0x1
    if data['is_shiny']: flag |= 0x2
    if data['is_break_after_fade']: flag |= 0x4
    if data['dummy']: flag |= 0x8
    return flag

def rebuild(data):
    # header
    head = BinaryReader()
    head.write_str('AIDB')
    head.write_uint32(33)  # endian check
    head.write_uint32(data['Version'])
    head.write_uint32(0)  # Padding
    head.write_uint32(len(data['Assets']))
    main_header_size = head.size() + ((len(data['Assets'])) * 4)
    sub_header_size = 256  # 64 * 4
    sub = BinaryReader()  # sub header
    for i in range(len(data['Assets'])):
        ass = BinaryReader()  # main data
        sub_data = data['Assets'][i]
        if 'Data' not in sub_data:
            head.write_uint32(0)
        else:
            head.write_uint32(main_header_size + sub.size())
            for o in range(64):
                if o < len(sub_data['Data']):
                    sub.write_uint32(sub_header_size + ass.size())
                    asset_data = sub_data['Data'][o]
                    ass.write_uint32(asset_data['Version'])
                    if o == 0:
                        ass.write_uint32(asset_data['PUID ID'])
                        ass.write_str_fixed(asset_data['Name'], size=16)
                        ass.write_uint32(asset_data['Broken asset PUID ID'])
                        ass.write_uint32(asset_data['Prog ID'])
                        ass.write_uint32(asset_data['Prog Sub ID'])
                        ass.write_uint8(asset_data['Arms Category'])
                        ass.write_uint8(asset_data['Arms Category Sub'])
                        ass.write_uint8(asset_data['Hand pattern'])
                        ass.write_int8(asset_data['Use count']) # TODO - rename to durability
                        ass.write_uint8(asset_data['Durability'])
                        ass.write_uint8(asset_data['Break blast param'])
                        ass.write_uint8(
                            asset_data['Durability Restraints Category'])
                        ass.write_uint8(0)  # padding
                        ass.write_int32(
                            asset_data['Broken random asset PUID ID'])
                        ass.write_int32(asset_data['Impact Power'])
                        ass.write_uint32(write_asset_id_flag(asset_data['Flags']))
                        ass.write_float(asset_data['Pickup offset X'])
                        ass.write_float(asset_data['Pickup offset Y'])
                        ass.write_float(asset_data['Pickup offset Z'])
                        ass.write_uint32(asset_data['Hact range'])
                        ass.write_uint64(0)  # padding
                    elif o == 1:
                        ass.write_uint32(asset_data['Model ID'])
                        ass.write_uint32(write_modeltype_flag(asset_data['Flags']))
                        ass.write_uint8(asset_data['Geometry type'])
                        ass.write_uint16(0)  # Padding
                        ass.write_uint8(0)  # Padding
                    elif o == 2:
                        if 'Texture replacement' in asset_data:
                            ass.write_uint32(
                                len(asset_data['Texture replacement']))
                        else:
                            ass.write_uint32(0)  # no entries
                        ass.write_uint64(0)  # padding
                        if 'Texture replacement' in asset_data:
                            for i in range(len(asset_data['Texture replacement'])):
                                tex = asset_data['Texture replacement'][i]
                                ass.write_str_fixed(
                                    tex['Base texture'], size=32)
                                ass.write_str_fixed(
                                    tex['Replacement texture'], size=32)
                    elif o == 3:
                        if 'Particle params' in asset_data:
                            ass.write_uint32(
                                len(asset_data['Particle params']))
                        else:
                            ass.write_uint32(0)  # no entries
                        ass.write_uint64(0)  # padding
                        if 'Particle params' in asset_data:
                            for i in range(len(asset_data['Particle params'])):
                                item = asset_data['Particle params'][i]
                                ass.write_uint32(item['Particle ID'])
                                ass.write_uint8(0)  # padding
                                ass.write_uint8(item['Timing'])
                                ass.write_uint8(item['Assign node'])
                                ass.write_uint8(0)  # padding
                                ass.write_uint8(item['color_r'])
                                ass.write_uint8(item['color_g'])
                                ass.write_uint8(item['color_b'])
                                ass.write_uint8(item['color_a'])
                                ass.write_uint32(write_particle_flag(item['Flags']))
                                ass.write_float(item['Shininess'])
                                ass.write_float(item['ioe'])
                                ass.write_uint64(0)  # padding
                    elif o == 4:
                        ass.write_uint8(asset_data['Move mode'])
                        ass.write_uint16(0)  # Padding
                        ass.write_uint8(0)  # Padding
                        ass.write_uint32(write_type_flag(asset_data['Flags']))
                        ass.write_float(asset_data['Move limit size'])
                        ass.write_int32(asset_data['Inclination limit param'])
                        ass.write_uint32(asset_data['Collision ID'])
                        ass.write_uint64(0)  # Padding
                    elif o == 5: # used in LJ, may be incorrect, testing needed
                        if 'Motion list' in asset_data:
                            ass.write_uint32(len(asset_data['Motion list']))
                        else:
                            ass.write_uint32(0)
                        ass.write_uint32(asset_data['Motion ID'])
                        if 'Motion list' in asset_data:
                            for item in asset_data['Motion list']:
                                ass.write_uint32(item['Unk1'])
                                ass.write_uint32(item['Unk2'])
                        ass.write_uint32(asset_data['Unk3'])  # Padding
                    elif o == 6:
                        if 'Asset Presets' in asset_data:
                            ass.write_uint32(len(asset_data['Asset Presets']))
                        else:
                            ass.write_uint32(0)
                        ass.write_uint32(write_presettype_flag(asset_data['Flags']))
                        ass.write_uint32(0)  # Padding
                        if 'Asset Presets' in asset_data:
                            for i in range(len(asset_data['Asset Presets'])):
                                item = asset_data['Asset Presets'][i]
                                ass.write_uint32(item['Asset ID'])
                                ass.write_float(item['px'])
                                ass.write_float(item['py'])
                                ass.write_float(item['pz'])
                                ass.write_float(item['ry'])
                                ass.write_float(item['rx'])
                                ass.write_float(item['rz'])
                                ass.write_uint32(0)  # Padding
                    elif o == 7:
                        ass.write_uint32(asset_data['Sound ID Category'])
                        ass.write_uint64(0)  # Padding
                        ass.write_uint64(0)  # Paddingy
                        ass.write_uint64(0)  # Padding
                    elif o == 8:
                        ass.write_uint32(write_display_flag(asset_data['Flags']))
                        ass.write_float(asset_data['UV offset U'])
                        ass.write_float(asset_data['UV offset V'])
                        ass.write_float(asset_data['Nearclip param'])
                        ass.write_uint8(
                            asset_data['Shadow occlusion luminance'])
                        ass.write_uint16(0)  # Padding
                        ass.write_uint8(0)  # Padding
                        ass.write_uint32(asset_data['Color change 1'])
                        ass.write_uint32(asset_data['Color change 2'])
                        ass.write_uint32(asset_data['Arm name'])
                        ass.write_float(asset_data['Scrap fade time'])
                        ass.write_uint32(asset_data['Effect highlight'])
                        ass.write_float(asset_data['LOD Factor HM'])
                        ass.write_float(asset_data['LOD Factor ML'])
                        ass.write_float(asset_data['Scale'])
                        ass.write_float(asset_data['Unk1']) # used in LJ
                        ass.write_uint32(asset_data['Unk2']) # used in LJ
                    elif o == 9:
                        if 'Lights' in asset_data:
                            ass.write_uint32(len(asset_data['Lights']))
                        else:
                            ass.write_uint32(0)  # no entries
                        ass.write_uint64(0)  # Padding
                        if 'Lights' in asset_data:
                            for i in range(len(asset_data['Lights'])):
                                item = asset_data['Lights'][i]
                                ass.write_uint64(item['WGP_uid'])
                                ass.write_uint8(0)  # Padding
                                ass.write_uint8(item['Timing'])
                                ass.write_uint16(0)  # Padding
                                ass.write_uint32(item['Node ID'])
                    elif o == 10:
                        if 'Effect event params' in asset_data:
                            ass.write_uint32(
                                len(asset_data['Effect event params']))
                        else:
                            ass.write_uint32(0)  # no entries
                        ass.write_uint64(0)  # Padding
                        if 'Effect event params' in asset_data:
                            for i in range(len(asset_data['Effect event params'])):
                                item = asset_data['Effect event params'][i]
                                ass.write_uint32(0)  # Padding
                                ass.write_uint32(item['Event ID'])
                                ass.write_uint64(0)  # Padding
                    elif o == 11:
                        if 'Animation params' in asset_data:
                            ass.write_uint32(
                                len(asset_data['Animation params']))
                        else:
                            ass.write_uint32(0)  # no entries
                        ass.write_uint64(0)  # Padding
                        if 'Animation params' in asset_data:
                            for i in range(len(asset_data['Animation params'])):
                                item = asset_data['Animation params'][i]
                                ass.write_uint32(item['Node id'])
                                ass.write_uint32(item['Axis'])
                                ass.write_float(item['Speed'])
                                ass.write_uint32(write_anim_flag(item['Flags']))
                                ass.write_int32(item['limitrot_l_dummy'])
                                ass.write_int32(item['limitrot_r_dummy'])
                                ass.write_float(item['limitrot_l'])
                                ass.write_float(item['limitrot_r'])
                    elif o == 12:
                        if 'dummy_bullet params' in asset_data:
                            asset_data['Item Count'] = ass.write_uint32(
                                len(asset_data['dummy_bullet params']))
                        else:
                            ass.write_uint32(0)  # no entries
                        ass.write_uint64(0)  # padding
                        if 'dummy_bullet params' in asset_data:
                            for i in range(len(asset_data['dummy_bullet params'])):
                                item = asset_data['dummy_bullet params'][i]
                                ass.write_uint32(item['Unk1'])
                                ass.write_uint32(item['Unk2'])
                                ass.write_uint32(item['Unk3'])
                                ass.write_uint32(item['Unk4'])
                    elif o == 13:
                        ass.write_uint32(asset_data['Arms padding'])
                        ass.write_uint8(asset_data['Arms category'])
                        ass.write_uint8(asset_data['Arms category sub'])
                        ass.write_uint16(0)  # Padding
                        ass.write_float(asset_data['Attack scale'])
                        ass.write_int32(asset_data['Impact Param'])
                        ass.write_int32(asset_data['Use count'])
                        ass.write_uint32(asset_data['Arm name'])
                        ass.write_uint32(write_attr_flag(asset_data['Attributes']))
                        ass.write_uint32(write_arms_flag(asset_data['Flags']))
                        ass.write_uint32(asset_data['Infinite Arms ID'])
                        ass.write_uint32(asset_data['Spray bomb'])
                        ass.write_uint32(asset_data['Another handle arms'])
                        ass.write_float(
                            asset_data['Grenade Explode Time Player'])
                        ass.write_float(
                            asset_data['Grenade Explode Time Else'])
                        ass.write_float(asset_data['Throw speed'])
                        ass.write_uint32(asset_data['Arms Parameter'])
                        for i in range(8):
                            ass.write_uint64(0)  # Padding
                    elif o == 14:
                        if 'Language texture replace list' in asset_data:
                            ass.write_uint32(
                                len(asset_data['Language texture replace list']))
                        else:
                            ass.write_uint32(0)  # no entries
                        ass.write_uint64(0)  # padding
                        if 'Language texture replace list' in asset_data:
                            for i in range(len(asset_data['Language texture replace list'])):
                                item = asset_data['Language texture replace list'][i]
                                ass.write_uint32(item['Texture PUID index'])
                                ass.write_uint64(0)  # padding
                                ass.write_uint32(0)  # padding
                    elif o == 15:
                        if 'Unknown list' in asset_data:
                            ass.write_uint32(len(asset_data['Unknown list']))
                            for item in asset_data['Unknown list']:
                                ass.write_uint32(item['Unk5'])
                        else:
                            ass.write_uint32(0) #no entries

                else:
                    sub.write_uint32(0)  # no pointer
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
                    json.dump(data, f, indent=2)
            file_count += 1

        print(f'{file_count} file(s) rebuilt.')
    else:
        input('You need to drag a file onto the script.\nPress ENTER to continue...')


if __name__ == "__main__":
    main()
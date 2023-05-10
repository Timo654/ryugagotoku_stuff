def tuple_str_to_int(item):
    return (int(item[0]), int(item[1]))

def get_type(str):
    str = str.lower().strip()
    if str == "false":
        return False
    elif str == 'true':
        return True
    elif str == 'none':
        return None
    else:
        raise ValueError("Unknown boolean found! -", str)

def atlas_parser(atlas_file):
    with open(atlas_file, 'r') as f:
        atlas_data = [x.strip() for x in f.readlines()]
    data = dict()
    data["tex_name"] = atlas_data[1]
    data["tex_size"] = tuple_str_to_int(atlas_data[2].replace("size: ", "").split(","))
    data["tex_format"] = atlas_data[3].replace("format: ", "")
    data["tex_filter"] = atlas_data[4].replace("filter: ", "").split(",")
    data["repeat"] = get_type(atlas_data[5].replace("repeat: ", ""))
    data["parts"] = list()
    for i in range(6, len(atlas_data[6:]), 7):
        part = dict()
        part["name"] = atlas_data[i]
        part["rotate"] = get_type(atlas_data[i+1].replace("rotate: ", ""))
        part["xy"] = tuple_str_to_int(atlas_data[i+2].replace("xy: ", "").split(","))
        part["size"] = tuple_str_to_int(atlas_data[i+3].replace("size: ", "").split(","))
        part["orig"] = tuple_str_to_int(atlas_data[i+4].replace("orig: ", "").split(","))
        part["offset"] = tuple_str_to_int(atlas_data[i+5].replace("offset: ", "").split(","))
        part["index"] = int(atlas_data[i+6].replace("index: ", ""))
        data["parts"].append(part)
    return data
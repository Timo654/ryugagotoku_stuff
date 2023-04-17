# Yakuza PS2 model format importer by Timo654, thanks to Kan, Violet and Jhrino for help in figuring stuff out

from inc_noesis import *

import noesis

# rapi methods should only be used during handler callbacks
import rapi

# library for my funny material workaround
import os
import json

# registerNoesisTypes is called by Noesis to allow the script to register formats.
# Do not implement this function in script files unless you want them to be dedicated format modules!


def registerNoesisTypes():
    handle = noesis.register("Yakuza PS2 models", ".ome")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadModel(handle, noepyLoadModel)
    # noesis.logPopup()
    return 1

# check if it's this type based on the data


def noepyCheckType(data):
    bs = NoeBitStream(data)
    header = bs.readBytes(3).decode("ASCII")
    if header != 'OME':
        return 0
    return 1


def load_mesh(bs, odbp_pointer, uv, weights, stage, mesh_count, current_material):
    weight_list = list()
    bs.seek(12, NOESEEK_REL)
    vertCount = bs.readInt()
    faceOff = odbp_pointer + bs.readInt() + 32
    faceCount = bs.readInt()
    bs.seek(8, NOESEEK_REL)
    vertBuff = bytes()
    normalBuff = bytes()
    if uv:
        uvBuff = bytes()
    for _ in range(vertCount):
        vert = NoeVec3.fromBytes(bs.readBytes(12))
        vertBuff += vert.toBytes()
        if stage:
            bs.seek(4, NOESEEK_REL)
        if weights:
            weight = bs.readFloat()
            bones = list()
            for _ in range(4):
                bones.append(bs.readByte())
            bones = [x for x in bones if x != 0]
            if len(bones) != 0:
                # weight = [weight / len(bones)] * len(bones)
                weight = [weight] * len(bones)
                weight_list.append(NoeVertWeight(bones, weight))
            else:
                weight_list.append(NoeVertWeight([0], [weight]))

        normal = NoeVec3.fromBytes(bs.readBytes(12))
        normalBuff += normal.toBytes()
        if uv:
            uvBuff += bs.readBytes(8)
    if len(weight_list) != 0:
        fw = NoeFlatWeights(weight_list)
        rapi.rpgBindBoneIndexBuffer(
            fw.flatW[:fw.weightValOfs], noesis.RPGEODATA_INT, 4*fw.weightsPerVert, fw.weightsPerVert)
        rapi.rpgBindBoneWeightBuffer(
            fw.flatW[fw.weightValOfs:], noesis.RPGEODATA_FLOAT, 4*fw.weightsPerVert, fw.weightsPerVert)
    rapi.rpgSetName('mesh_' + str(mesh_count))
    if current_material != None:
        rapi.rpgSetMaterial(current_material)
    print(current_material)
    rapi.rpgBindPositionBuffer(vertBuff, noesis.RPGEODATA_FLOAT, 12)
    rapi.rpgBindNormalBuffer(normalBuff, noesis.RPGEODATA_FLOAT, 12)
    if uv:
        rapi.rpgBindUV1Buffer(uvBuff, noesis.RPGEODATA_FLOAT, 8)
    bs.seek(faceOff)
    FaceBuff = bs.readBytes(faceCount * 2)
    rapi.rpgCommitTriangles(FaceBuff, noesis.RPGEODATA_USHORT,
                            faceCount, noesis.RPGEO_TRIANGLE_STRIP, 1)
    if current_material != None:
        NoeMaterial(current_material[:-4], current_material)


def add_bones(bs, base_pointer, bone_info_pointer, bone_count):
    boneList = list()
    bones = dict()
    bs.seek(base_pointer + bone_info_pointer)
    for i in range(bone_count):
        #print("CURRENT POS:", bs.tell())
        bone_ptr = bs.tell() - base_pointer
        bones[bone_ptr] = dict()
        # not sure what to do with these
        #vector1 = bs.readBytes(16)
        #vector2 = bs.readBytes(16)
        bs.seek(32, NOESEEK_REL)
        bones[bone_ptr]["Child"] = bs.readUInt()
        bones[bone_ptr]["Sibling"] = bs.readUInt()
        bones[bone_ptr]["ID"] = bs.readUInt()
        bs.seek(4, NOESEEK_REL)
        transform = list()
        for i in range(3):
            if i == 2:
                # this flips the skeleton. we do this because yakuza models are flipped and flipax does not flip the skeleton
                transform.append(-bs.readFloat())
            else:
                transform.append(bs.readFloat())
        bs.seek(4, NOESEEK_REL)

        myQuat = NoeQuat().toMat43()
        myQuat[3] = tuple(transform)
        bs.seek(16, NOESEEK_REL)
        bones[bone_ptr]["Parent"] = -1
        bones[bone_ptr]["Transform"] = myQuat

    # update parents
    for bone in bones:
        if bones[bone]["Child"] != 0:
            child_bone = bones[bones[bone]["Child"]]
            child_bone["Parent"] = bones[bone]["ID"]
            if child_bone["Sibling"] != 0:
                update_sibling(
                    bones, bones[child_bone["Sibling"]], bones[bone]["ID"])

    for bone in bones:
        boneList.append(NoeBone(bones[bone]["ID"], "bone_" + str(
            bones[bone]["ID"]), bones[bone]["Transform"], parentIndex=bones[bone]["Parent"]))

    return boneList
# load the model


def update_sibling(bones, bone, parent_id):
    bone["Parent"] = parent_id
    if bone["Sibling"] != 0:
        update_sibling(bones, bones[bone["Sibling"]], parent_id)


def noepyLoadModel(data, mdlList):
    rapi.rpgCreateContext()
    boneList = list()
    model_dir = os.path.dirname(rapi.getInputName())
    mat_file = os.path.join(model_dir, 'materials.txt')
    manifest_file = os.path.join(model_dir, 'manifest.json')
    current_material = None
    model_name = os.path.basename(rapi.getInputName()) 
    if os.path.exists(mat_file):
        print('Found materials.txt file, reading that.')
        with open(mat_file, 'r') as f:
            mat_data = f.readlines()
        for material in mat_data:
            material = material.strip().split(':')
            if material[0] == model_name:
                current_material = material[1]
                break
    elif os.path.exists(manifest_file):
        with open(manifest_file, "r") as f:
            manifest_data = json.load(f)
            txbs = list()
            omes = list()
            for key in manifest_data:
                if key.startswith("Section"):
                    if manifest_data[key]["Identifier"] == "TLFD":
                        for item in manifest_data[key]:
                            if item.isnumeric():
                                if manifest_data[key][item]["Path"].lower().endswith("txb"):
                                    txbs.append(
                                        manifest_data[key][item]["Path"])
                                elif manifest_data[key][item]["Path"].lower().endswith("ome"):
                                    omes.append(
                                        manifest_data[key][item]["Path"])
            if model_name in omes:
                index = omes.index(model_name)
                if index < len(txbs):
                    current_material = txbs[omes.index(
                    model_name)]
                    print("Found texture from manifest.json.")
                    print(current_material)
    else:   
        print('No materials.txt found.')

    stage = False
    mesh_count = 0
    bs = NoeBitStream(data)
    bs.setEndian(NOE_LITTLEENDIAN)
    bs.seek(8)
    odbp_pointer = bs.readUInt()
    bs.seek(odbp_pointer + 48)
    is_uv = bs.readByte()
    if is_uv == 66:
        uv = False
    elif is_uv == 22:
        print('Most likely a stage model')
        uv = True
        stage = True
    else:
        uv = True
    if bs.readByte() == 1 or stage:
        weights = False
    else:
        weights = True
    #print('weights', weights)
    #print('UVs', uv)

    bs.seek(odbp_pointer + 32)
    mesh_info_pointer = bs.readUInt()
    mesh_count = bs.readUInt()

    bone_info_pointer = bs.readUInt()
    bone_count = bs.readUInt()

    boneList = add_bones(bs, odbp_pointer, bone_info_pointer, bone_count)

    bs.seek(odbp_pointer + mesh_info_pointer)
    mesh_pointers = list()
    for i in range(mesh_count):
        bs.seek(0x20, NOESEEK_REL)
        mesh_pointers.append(bs.readUInt())
        bs.seek(28, NOESEEK_REL)

    for index, mesh in enumerate(mesh_pointers):
        bs.seek(odbp_pointer + mesh + 0x20)
        load_mesh(bs, odbp_pointer, uv, weights,
                  stage, index, current_material)

    mdl = rapi.rpgConstructModel()
    mdl.setBones(boneList)
    mdlList.append(mdl)
    rapi.processCommands("-flipax 3")
    rapi.rpgClearBufferBinds()
    return 1

import os
import shutil
import sys

def Convert(string): 
    list1=[] 
    list1[:0]=string 
    return list1


if len(sys.argv) == 1:
    input("You need to specify a folder!\nPress ENTER to continue...")
    quit()
folder = sys.argv[1]

subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]

for o in range (0, len(subfolders)):
    model_str = Convert(os.path.basename(os.path.normpath(subfolders[o])))
    model_type = model_str[7]
    if model_type == 'h':
        model_type = 'head'
    else:
        model_type = 'body'
    if not os.path.exists(os.path.join(folder, model_type, os.path.basename(os.path.normpath(subfolders[o])))):
        os.makedirs(os.path.join(folder, model_type, os.path.basename(os.path.normpath(subfolders[o]))))

    for file in os.listdir(subfolders[o]):
        try:
            os.rename(os.path.join(subfolders[o], file), (os.path.join(folder, model_type, os.path.basename(os.path.normpath(subfolders[o])), file)))
        except(FileExistsError):
            print('Folder ' + os.path.basename(os.path.normpath(subfolders[o])) + ' could not be renamed.')

    shutil.rmtree(subfolders[o])
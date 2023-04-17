import os
import shutil
import sys

if len(sys.argv) == 1:
    input("You need to specify a folder!\nPress ENTER to continue...")
    quit()

subfolders = [ f.path for f in os.scandir(sys.argv[1]) if f.is_dir() ]

new_folders = []
for p in range (0, len(subfolders)):
    new_folders.append((subfolders[p].split("_", 1)[0]))
print(new_folders)
for o in range (0, len(new_folders)):
    print(subfolders[o])
    if len(os.path.basename(os.path.normpath(subfolders[o]))) == 4:
        pass
    else:
        if os.path.exists(new_folders[o]):
            for file in os.listdir(subfolders[o]):
                try:
                    os.rename(os.path.join(subfolders[o], file), os.path.join(new_folders[o], file))
                except(FileExistsError):
                    print('Folder ' + os.path.basename(os.path.normpath(subfolders[o])) + ' could not be renamed.') 
            shutil.rmtree(subfolders[o])
        else:
            os.rename(subfolders[o], new_folders[o])
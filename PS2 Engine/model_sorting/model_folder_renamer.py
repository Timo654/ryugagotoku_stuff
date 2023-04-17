import os
from pathlib import Path
path = input("Enter the model directory: ")

first_model_list = input("Enter the first model list filename: ")
second_model_list = input("Enter the second model list filename: ")
with open(first_model_list) as f:
    first_modelnames = f.read().splitlines()

with open(second_model_list) as f:
    second_modelnames = f.read().splitlines()

characters = []
for file in os.listdir(path):
    d = os.path.join(path, file)
    if os.path.isdir(d):
        characters.append(d)

for i in range (0, len(first_modelnames)):
    for file in os.listdir(characters[i]):
        if file.endswith(('0.dat', '0.bin', '2.dat', '2.bin', '4.dat', '4.bin')):
            if not os.path.exists(characters[i] + '_' + first_modelnames[i]):
                os.makedirs(characters[i] + '_' + first_modelnames[i])

            os.rename(os.path.join(characters[i], file), os.path.join((characters[i] + '_' + first_modelnames[i]), file))

        elif file.endswith(('1.dat', '1.bin', '3.dat', '3.bin', '5.dat', '5.bin')):
            if not os.path.exists(characters[i] + '_' + second_modelnames[i]):
                os.makedirs(characters[i] + '_' + second_modelnames[i])

            os.rename(os.path.join(characters[i], file), os.path.join((characters[i] + '_' + second_modelnames[i]), file))

for file in characters:
    Path(file).rmdir()
    
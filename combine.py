import os
import shutil
import secret
import json

stack = [secret.TO_ADD]
dirstack = []

#create lookup table for if file exists
with open(os.path.join(secret.DESTPATH,"downloadedfiles.json"), 'r') as f:
        downloaded_files = json.load(f)
        downloaded_files = list(map(lambda x: x[1:], downloaded_files))

with open(os.path.join(secret.DESTPATH,"filequeue.json"), 'r') as f:
        fqueue = json.load(f)

file_list = fqueue + downloaded_files
keys = dict(zip(file_list, [True for i in range(len(file_list))])).keys()

pathstack = [""]
foundstack = []

while True:
    if pathstack == []:
        break
    currentpath = pathstack.pop()
    full_path = os.path.join(secret.TO_ADD, currentpath)
    for filename in os.listdir(full_path):
        if os.path.isdir(os.path.join(full_path, filename)):
            pathstack.append(os.path.join(currentpath, filename))
        elif filename.endswith(".html"):
            foundstack.append(os.path.join(currentpath, filename))

files_to_copy = []
for file in foundstack:
    if file not in file_list:
        fqueue.append(file)
        files_to_copy.append(file)

for file in files_to_copy:
    src = os.path.join(secret.TO_ADD, file)
    dest = os.path.join(secret.DESTPATH, "files", file)
    shutil.copyfile(src, dest)
    print(f"{src} -> {dest}")

with open(os.path.join(secret.DESTPATH,"filequeue.json"), 'r') as f:
    json.dump(fqueue, f)










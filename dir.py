import os

path = os.path.abspath('.')

files = []
for entry in os.scandir(path):
    if entry.is_file():
        files.append(os.path.join(path, entry))


for f in files:
    print(f)
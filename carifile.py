import os

target = "MEmuConsole.exe"
found = []

# daftar drive umum di Windows
drives = ["C:\\", "D:\\", "E:\\"]

for drive in drives:
    for root, dirs, files in os.walk(drive):
        if target in files:
            found.append(os.path.join(root, target))

if found:
    print("Ditemukan di:")
    for path in found:
        print(path)
else:
    print("MEmuConsole.exe tidak ditemukan di C, D, atau E drive.")

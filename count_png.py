import os
from common import *

if __name__ == '__main__':
    sha256_list = []
    last_files = getFileList(OutputCGAPI, ".csv")
    for file in last_files:
        apkname = os.path.split(file)[-1][:-4]
        sha256_list.append(apkname)

    files = getFileList(CODE_ICON_PATH, ".png")
    new_list = []
    for file in files:
        apkname = file.split('/')[-2]
        if apkname in sha256_list:
            new_list.append(apkname)
    print(len(new_list))
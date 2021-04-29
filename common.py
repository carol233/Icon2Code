# coding:utf-8
import hashlib
import os
import csv
csv.field_size_limit(100000000)
TrainingSet = "/home/yanjie/gator-3.8/FilteringDataset"
ANDROZOO_CSV_PATH = "/mnt/fit-Knowledgezoo/Patrick/latest/latest.csv"
APKPATH = "/mnt/fit-Knowledgezoo/yanjie/APK_with_DESC"
CODE_ICON_PATH = "/home/yanjie/gator-3.8/ICON_CODE"
Database_name = "data.db"
New_database_name = "newdata.db"
APKInfo_db_name = "info.db"
Dataset_split_path = "10_fold"
OutputLibScout = "OutputLibScout/"
aapt = "/home/yanjie/android-sdk-linux/build-tools/30.0.0-preview/aapt"
andro_jar = "/home/yanjie/android-sdk-linux/platforms"
OutputCGAPI = "OutputCGAPI/"
nodejs_path = ""


def getFileList(rootDir, pick_str):
    """
    :param rootDir:  root directory of dataset
    :return: A filepath list of sample
    """
    filePath = []
    for parent, dirnames, filenames in os.walk(rootDir):
        for filename in filenames:
            if filename.endswith(pick_str):
                file = os.path.join(parent, filename)
                filePath.append(file)
    return filePath


def getFileList2(rootDir, start_str, end_str):
    """
    :param rootDir:  root directory of dataset
    :return: A filepath list of sample
    """
    filePath = []
    for file in os.listdir(rootDir):
        if file.startswith(start_str) and file.endswith(end_str):
            filename = os.path.join(rootDir, file)
            filePath.append(filename)
    return filePath


def get_sha256(s):
    m = hashlib.sha256()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def dict2sortedlist(dic: dict):
    lst = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    return lst


def writeScores(saveDir, project_name, score_list):
    with open(os.path.join(saveDir, str(project_name) + ".csv"), "w", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerows(score_list)


def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for _ in in_file)


def check_and_mk_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_md5(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def get_pic_path(f, apk_sha256):
    icon_type = os.path.splitext(f)[-1]  # start with .
    new_icon_name = get_md5(f) + icon_type
    codepath_apkname = os.path.join(CODE_ICON_PATH, apk_sha256)
    path_new = os.path.join(codepath_apkname, new_icon_name)
    return path_new
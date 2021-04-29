from DataReader import DataReader
from common import *
import pexpect

APK_paths = "/mnt/fit-Knowledgezoo/yanjie/APK_with_DESC"
passwd = "changeme"
Download_paths = "/Users/yzha0544/PycharmProjects/VD/in/"
script_filename = "download_log"
fout = open(script_filename, "wb")

if __name__ == '__main__':
    dataread = DataReader(Database_name)
    datas = dataread.query_all()
    dataread.close()
    APK_list = []

    for item in datas:
        APK_list.append(datas[item][5])

    APK_list = list(set(APK_list))

    for APK in APK_list:
        CMD = "scp yanjie@130.194.181.38:" + os.path.join(APK_paths, APK + '.apk') + " " + Download_paths

        child = pexpect.spawn(CMD)
        child.logfile = fout
        index = child.expect(['password', pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            child.sendline(passwd)
            downloadindex = child.expect(['.apk', pexpect.EOF], timeout=120)
            print(APK)
        elif index == 1:
            print("EOF!")
        else:
            print("Time out!")
        child.close(force=True)

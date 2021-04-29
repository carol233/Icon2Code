# coding:utf-8
import random
import sqlite3
import subprocess
import threadpool
from common import *
import re


class PresolveAPK:
    def __init__(self, Training_set, APKPATH, maxjob, output_dir, aapt, android_jars):
        self.training_set = Training_set
        self.APKpath = APKPATH
        self.max_jobs = maxjob
        self.save_path = output_dir
        self.aapt = aapt
        self.android_jars = android_jars
        self.all = 0

    def processone(self, apk):
        query_targetsig = Query("data.db")
        query_pkgname = Query("info.db")
        apkname = os.path.split(apk)[-1][:-4]
        apkpath = os.path.join(self.APKpath, apkname + ".apk")
        output_path = os.path.join(self.save_path, apkname + ".csv")
        if os.path.exists(output_path):
            print("[+] " + apkname + " exists!")
            return

        # try:
        #     AAPT_CMD = self.aapt + " dump badging " + apkpath + "| grep package:\ name"
        #     output = subprocess.check_output(AAPT_CMD, shell=True, timeout=20)
        # except subprocess.TimeoutExpired as exc:
        #     print("Command timed out: {}".format(exc))
        #     return
        # except subprocess.CalledProcessError as e:
        #     output = e.output  # Output generated before error
        #     code = e.returncode  # Return code
        #     return
        #
        # aapt_output = output.decode('utf-8')
        # """ EXAMPLE
        # package: name='com.example.myapplication' versionCode='1'
        # versionName='1.0' compileSdkVersion='29' compileSdkVersionCodename='10'
        # """
        #
        # pkg = re.findall(r"package: name='([0-9a-zA-Z.]+)'", aapt_output)
        # if pkg:
        #     pkgname = pkg[0]
        #     print("[+] " + pkgname)
        # else:
        #     return

        pkgname = query_pkgname.select_pkgname(apkname)
        if not pkgname:
            print("pkgname error!")
            return

        targetSig = query_targetsig.select_query(apkname)
        if not targetSig:
            print("targetSig error!")
            return

        try:
            print("[+] PreSolving " + apkname)
            CMD = "java -Xms1024m -Xmx4096m -XX:MaxNewSize=2048m " \
                  "-jar Lib/IconHunter.jar " \
                  + apkpath + " " + pkgname + " \"" + targetSig + "\" " \
                  + self.android_jars + " " + os.path.join(self.save_path, apkname + ".csv")
            subprocess.run(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           encoding="utf-8", timeout=90)
        except subprocess.TimeoutExpired as exc:
            print("Command timed out: {}".format(exc))
        except Exception as e:
            print(e)

        if os.path.exists(output_path):
            row_num = row_count(output_path)
            if row_num == 1:
                os.remove(output_path)

    def start(self):
        apks = getFileList(self.training_set, ".csv")
        random.shuffle(apks)
        self.all = len(apks)

        print("[+] Total apks ", self.all)
        print("[+] Saving results to " + self.save_path)

        args = [(apk) for apk in apks]
        pool = threadpool.ThreadPool(self.max_jobs)
        requests = threadpool.makeRequests(self.processone, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()


class Query:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)

    def select_query(self, sha256):
        newlist = []
        cu = self.conn.cursor()
        sql = """select HANDLER from DATA where APK_SHA256 = '""" + sha256 + """'"""
        results = cu.execute(sql)
        tmplist = results.fetchall()
        for item in tmplist:
            newlist.extend(item[0].split(";"))
        return ";".join(list(set(newlist)))

    def select_pkgname(self, sha256):
        res = ""
        cu = self.conn.cursor()
        sql = """select PACKAGE_NAME from INFO where APK_SHA256 = '""" + sha256 + """'"""
        results = cu.execute(sql)
        tmplist = results.fetchall()
        for item in tmplist:
            res = item[0]
        return res


if __name__ == '__main__':
    if os.path.exists(OutputCGAPI):
        files = getFileList(OutputCGAPI, ".csv")
        for file in files:
            row_num = row_count(file)
            if row_num == 1:
                os.remove(file)

    check_and_mk_dir(OutputCGAPI)
    prosolve = PresolveAPK(TrainingSet, APKPATH, 15, OutputCGAPI, aapt, andro_jar)
    prosolve.start()


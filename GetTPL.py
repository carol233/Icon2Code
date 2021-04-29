# LibScout
import re
import sqlite3
import os
import string
import subprocess
import threadpool
import threading
from common import *


class GetTPL:
    def __init__(self, database_db):
        self.db_name = database_db
        self.lock = threading.Lock()
        self.max_job = 20
        self.total_insert = 0

    def connect_database(self):
        """
        :param database: filepath of database
        :return: sqlite connection
        """
        conn = sqlite3.connect(self.db_name)
        print("Opened database successfully")

        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS INFO
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      APK_SHA256    TEXT    NOT NULL,
                      PACKAGE_NAME  TEXT,
                      minSdkVersion TEXT,
                      targetSdkVersion TEXT
                      );""")
        print("Table created successfully")
        conn.commit()
        self.conn = conn
        self.insert_count = 0
        self.sql_data = []

    def process_one(self, args):
        result = {}
        apk = args
        apkname = os.path.split(apk)[-1][:-4]
        if os.path.exists(os.path.join(OutputLibScout, apkname)):
            return None
        apk_path = os.path.join(APKPATH, apkname + ".apk")
        """
        java -Xms1024m -Xmx4096m -XX:PermSize=1024m -XX:MaxPermSize=2048m -XX:MaxNewSize=2048m -jar ./LibScout/build/libs/LibScout.jar -o match -p ./LibScout-Profiles -c ./LibScout/config/LibScout.toml -a ./LibScout/sdk/android.jar aaa.apk
        """
        try:
            CMD = "java -Xms1024m -Xmx4096m -XX:MaxNewSize=2048m " \
                  "-jar ./LibScout/build/libs/LibScout.jar -o match " \
                  "-p ./LibScout-Profiles -c ./LibScout/config/LibScout.toml " \
                  "-a ./LibScout/sdk/android.jar -j ./jsonOutput " + apk_path
            out_bytes = subprocess.check_output(CMD, shell=True)
        except subprocess.CalledProcessError as e:
            out_bytes = e.output  # Output generated before error
            code = e.returncode  # Return code
        out_text = out_bytes.decode('utf-8')

        res = re.findall(r'LibraryIdentifier\s+:\s+Package name:\s+(\S+)\s+', out_text)
        if res:
            result['PACKAGE_NAME'] = res[0]
        else:
            return None

        res = re.findall(r'LibraryIdentifier\s+:\s+minSdkVersion:\s+(\S+)\s+', out_text)
        if res:
            result['minSdkVersion'] = res[0]
        else:
            return None

        res = re.findall(r'LibraryIdentifier\s+:\s+targetSdkVersion:\s+(\S+)\s+', out_text)
        if res:
            result['targetSdkVersion'] = res[0]
        else:
            return None

        result['APK_SHA256'] = apkname

        pkg_name = result['PACKAGE_NAME']
        check_dir = os.path.join("./jsonOutput", "/".join(pkg_name.split(".")))
        if os.path.exists(check_dir):
            subprocess.call(["mv", check_dir, os.path.join(OutputLibScout, apkname)])
        return result

    def save_result(self, request, res):
        # if catch exception
        if not res:
            return

        self.lock.acquire()
        self.total_insert += 1

        if self.total_insert % 20 == 0:
            print(self.total_insert)

        row = (res['APK_SHA256'], res['PACKAGE_NAME'], res['minSdkVersion'], res['targetSdkVersion'])
        if self.insert_count > 400:
            self.sql_data.append(row)
            # sql = """UPDATE DATA SET DEX_MD5 = ? WHERE PATH like ?"""
            sql = """INSERT INTO INFO(APK_SHA256, PACKAGE_NAME, minSdkVersion, targetSdkVersion)
                  VALUES(?,?,?,?)"""
            cursor = self.conn.cursor()
            cursor.executemany(sql, self.sql_data)
            self.conn.commit()
            self.sql_data = []
            self.insert_count = 0
        else:
            self.insert_count += 1
            self.sql_data.append(row)

        self.lock.release()

    def start(self):
        self.connect_database()
        apks = getFileList(TrainingSet, ".csv")
        print("total files ", len(apks))
        args = [(apk) for apk in apks]
        pool = threadpool.ThreadPool(self.max_job)
        requests = threadpool.makeRequests(self.process_one, args, self.save_result)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    check_and_mk_dir(OutputLibScout)
    database = GetTPL(APKInfo_db_name)
    database.start()
    database.close()




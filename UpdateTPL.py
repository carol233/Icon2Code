import random
import re
import sqlite3
import json
import threadpool

from common import *

class UpdateTPL:

    def __init__(self, CGAPI_dir, TPL_path, db_name):
        self.check_path = CGAPI_dir
        self.TPL_path = TPL_path
        self.db_name = db_name
        self.max_jobs = 15

    def processone(self, apk):
        apkname = os.path.split(apk)[-1][:-4]
        TPL_single_dir = os.path.join(self.TPL_path, apkname)
        if not os.path.exists(TPL_single_dir):
            return
        json_files = getFileList(TPL_single_dir, ".json")

        db = DatabaseOperation(self.db_name)
        res_dict = db.select_query(apkname)
        if not res_dict:
            db.close()
            return

        handler2API = {}
        with open(apk, "r") as fr:
            reader = csv.reader(fr)
            headings = next(reader)
            for line in reader:
                APIs = line[1].strip('\"\'[] ')
                pattern = r'(<.*?>)'
                mi = re.findall(pattern, APIs)
                mi = list(set(mi))
                handler2API[line[0]] = mi

        all_TPLs = []
        for json_file in json_files:
            with open(json_file, "r") as fr:
                load_dict = json.load(fr)
            # if "lib_matches" in load_dict:
            #     lib_matches = load_dict["lib_matches"]
            #     for item in lib_matches:
            #         if "libRootPackage" in item:
            #             all_TPLs.append(item["libRootPackage"])
            if "lib_packageOnlyMatches" in load_dict:
                lib_packageOnlyMatches = load_dict["lib_packageOnlyMatches"]
                for item in lib_packageOnlyMatches:
                    all_TPLs.append(lib_packageOnlyMatches[item].strip('\"\' '))

        all_TPLs = list(set(all_TPLs))
        if not all_TPLs:
            db.close()
            return

        handler2TPL = {}
        for handler in handler2API:
            handler2TPL[handler] = []
            tmplist = handler2API[handler]
            for api in tmplist:
                for tpl in all_TPLs:
                    if tpl in api:
                        print(tpl, api)
                        handler2TPL[handler].append(tpl)
            tmp_tpls = handler2TPL[handler]
            if tmp_tpls:
                handler2TPL[handler] = list(set(tmp_tpls))
            else:
                handler2TPL.pop(handler)

        if not handler2TPL:
            db.close()
            return

        for item in res_dict:
            single_tpls = []
            tmp_list = res_dict[item][7].split(";")
            for handler in tmp_list:
                if handler in handler2TPL:
                    single_tpls.extend(handler2TPL[handler])
            str_tpls = ";".join(list(set(single_tpls)))
            db.update_lib(item, str_tpls)
        db.close()

    def start(self):
        apks = getFileList(self.check_path, ".csv")
        random.shuffle(apks)
        self.all = len(apks)
        print("[+] Total apks ", self.all)

        args = [(apk) for apk in apks]
        pool = threadpool.ThreadPool(self.max_jobs)
        requests = threadpool.makeRequests(self.processone, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()


class UpdateAPI:
    def __init__(self, CGAPI_dir, TPL_path, db_name):
        self.check_path = CGAPI_dir
        self.TPL_path = TPL_path
        self.db_name = db_name
        self.max_jobs = 1

    def processone(self, apk):
        apkname = os.path.split(apk)[-1][:-4]
        # json_files = getFileList(TPL_single_dir, ".json")

        db = DatabaseOperation(self.db_name)
        res_dict = db.select_query(apkname)
        db.close()
        if not res_dict:
            return

        handler2API = {}
        with open(apk, "r") as fr:
            reader = csv.reader(fr)
            headings = next(reader)
            for line in reader:
                APIs = line[1].strip('\"\'[] ')
                pattern = r'(<.*?>)'
                mi = re.findall(pattern, APIs)
                if mi:
                    mi = list(set(mi))
                    handler2API[line[0]] = mi

        rows = []
        for item in res_dict:
            single_apis = []
            tmp_list = res_dict[item][7].split(";")
            for handler in tmp_list:
                if handler in handler2API:
                    single_apis.extend(handler2API[handler])
            str_apis = ";".join(list(set(single_apis)))
            if str_apis:
                rows.append((str_apis, "2", item))
        if rows:
            db = DatabaseOperation(self.db_name)
            # print(rows)
            db.update_many_libs(rows)
            db.close()

    def start(self):
        apks = getFileList(self.check_path, ".csv")
        random.shuffle(apks)
        self.all = len(apks)
        print("[+] Total apks ", self.all)

        args = [(apk) for apk in apks]
        pool = threadpool.ThreadPool(self.max_jobs)
        requests = threadpool.makeRequests(self.processone, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()


class Update_API_LEVEL:

    def __init__(self, dataDB, infoDB):
        self.dataDB = DatabaseOperation(dataDB)
        self.infoDB = DatabaseOperation(infoDB)

    def start(self):
        APK_info = self.infoDB.query_all_info()
        for sha256 in APK_info:
            hash2data = self.dataDB.select_query(sha256)
            if not hash2data:
                continue
            detail = list(APK_info[sha256])
            targetSDK = detail[-1]
            minSDK = detail[-2]
            for item in hash2data:
                self.dataDB.update_LEVEL(item, minSDK, targetSDK)


class DatabaseOperation:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)

    def select_all_data(self):
        res_dict = {}
        cu = self.conn.cursor()
        sql = """select * from DATA where FLAG = '2' """
        results = cu.execute(sql)
        tmplist = results.fetchall()
        for item in tmplist:
            res_dict[item[0]] = item
        return res_dict

    def select_query(self, sha256):
        res_dict = {}
        cu = self.conn.cursor()
        sql = """select * from DATA where APK_SHA256 = '""" + sha256 + """' and FLAG = '2' """
        results = cu.execute(sql)
        tmplist = results.fetchall()
        for item in tmplist:
            res_dict[item[0]] = item
        return res_dict

    def update_LEVEL(self, Id, minSDK, targetSDK):
        row = (str(minSDK) + "-" + str(targetSDK), Id)
        cu = self.conn.cursor()
        sql = """UPDATE DATA SET API_LEVEL = ? WHERE ID = ?"""
        cu.execute(sql, row)
        self.conn.commit()

    def update_lib(self, Id, libs: str):
        row = (libs, "2", Id)
        cu = self.conn.cursor()
        sql = """UPDATE DATA SET LIBRARY = ?, FLAG = ?  WHERE ID = ?"""
        cu.execute(sql, row)
        self.conn.commit()

    def update_many_libs(self, rows):
        cu = self.conn.cursor()
        sql = """UPDATE DATA SET LIBRARY = ?, FLAG = ? WHERE ID = ?"""
        cu.executemany(sql, rows)
        self.conn.commit()

    def query_all_info(self):
        res_dict = {}
        cu = self.conn.cursor()
        sql = """select * from INFO """
        results = cu.execute(sql)
        tmplist = results.fetchall()
        for item in tmplist:
            res_dict[item[1]] = item
        return res_dict

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # updateAPI = Update_API_LEVEL(Database_name, APKInfo_db_name)
    # updateAPI.start()

    # updateTPL = UpdateTPL(OutputCGAPI, OutputLibScout, Database_name)
    # updateTPL.start()

    updateLib = UpdateAPI(OutputCGAPI, OutputLibScout, Database_name)
    updateLib.start()

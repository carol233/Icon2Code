import math
import random
import sqlite3
from common import *

class DataReader:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.datas = {}
        self.index = []
        self.length = 0
        self.generate = 0

    def reset_generate(self):
        self.generate = 1

    def query_all(self):
        cu = self.conn.cursor()
        sql = """SELECT * FROM DATA WHERE LIBRARY != ''  and FLAG = '2' """
        results = cu.execute(sql)
        datas = results.fetchall()
        for item in datas:
            if self.generate:
                apis = list(item)[-2].split(';')
                if len(apis) >= 4:  # the median
                    self.datas[int(item[0])] = item
                    self.index.append(int(item[0]))
            else:
                self.datas[int(item[0])] = item
                self.index.append(int(item[0]))
        self.length = len(self.datas)
        print(self.length)
        return self.datas

    def query_detail(self, sha256, ICON_TYPE, API_LEVEL, EVENT, test_groups, flag):
        res = []
        cu = self.conn.cursor()
        sql1 = """SELECT * FROM DATA WHERE APK_SHA256 != '""" + sha256 + """' and 
                    ICON_TYPE = '""" + ICON_TYPE + """' and 
                    EVENT =  '""" + EVENT + """' and LIBRARY != '' and FLAG = '2' """

        sql2 = """SELECT * FROM DATA WHERE ICON_TYPE = '""" + ICON_TYPE + """' and 
                            EVENT =  '""" + EVENT + """' and LIBRARY != '' and FLAG = '2' """
        if flag == 1:
            results = cu.execute(sql1)
        else:
            results = cu.execute(sql2)
        datas = results.fetchall()
        for line in datas:
            index = int(line[0])
            if index in test_groups:
                continue
            if not API_LEVEL or not line[10]:
                res.append(index)
                continue
            tmp_1 = API_LEVEL.split("-")
            min1 = int(tmp_1[0])
            max1 = int(tmp_1[1])
            tmp_2 = line[10].split("-")
            min2 = int(tmp_2[0])
            max2 = int(tmp_2[1])
            if set(range(min1, max1)).issubset(set(range(min2, max2))):
                res.append(index)
        return res

    def query_single(self, index):
        row = (index)
        cu = self.conn.cursor()
        sql = """SELECT * FROM DATA WHERE ID = ? and FLAG = '2' """
        results = cu.execute(sql, row)
        line = list(results.fetchone())
        library = line[-2].split(";")
        return library

    def cut_k_fold(self, k):
        n = int(math.ceil(self.length * 1.0 / k))
        random.shuffle(self.index)
        list_of_groups = [self.index[i: i + n] for i in range(0, self.length, n)]
        self.recordGroups(list_of_groups, k)

    def recordGroups(self, list_of_groups, k):
        for i in range(k):
            record_file = os.path.join(Dataset_split_path, str(i) + ".txt")
            with open(record_file, "w") as fw:
                print(len(list_of_groups[i]))
                for item in list_of_groups[i]:
                    fw.write(str(item) + "\n")
        record_file1 = os.path.join(Dataset_split_path, "all.txt")
        with open(record_file1, "w") as fw:
            for item in self.index:
                fw.write(str(item) + "\n")

    def close(self):
        self.conn.close()

    def datasetGenerator(self, k):
        self.query_all()
        self.cut_k_fold(k)


if __name__ == "__main__":
    check_and_mk_dir(Dataset_split_path)
    dataReader = DataReader(Database_name)
    # dataReader.reset_generate()
    dataReader.datasetGenerator(10)

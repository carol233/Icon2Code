import re
import sqlite3
import os
import string
import threadpool
import threading
from common import *
from Helper.scrapAPK import *
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langdetect import detect_langs

class Database:
    def __init__(self, database_db):
        self.db_name = database_db
        self.lock = threading.Lock()
        self.max_job = 20
        self.total_insert = 0
        self.scrapAPK = ScrapAPK()
        self.scrapAPK.get_pkg_map(ANDROZOO_CSV_PATH)

    def connect_database(self):
        """
        :param database: filepath of database
        :return: sqlite connection
        """
        conn = sqlite3.connect(self.db_name)
        print("Opened database successfully")

        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS DATA
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      PIC_NAME      TEXT    NOT NULL,
                      IDNAME        TEXT    NOT NULL,
                      ICON_TYPE     TEXT    NOT NULL,
                      TEXT_ON_ICON  TEXT,
                      APK_SHA256    TEXT    NOT NULL,
                      EVENT         TEXT,
                      HANDLER       TEXT,
                      PIC_PATH      TEXT,
                      CODE_BODY     TEXT,
                      API_LEVEL     TEXT,
                      SUMMARY       TEXT,
                      DESCRIPTION   TEXT,
                      SCORE         TEXT, 
                      INSTALLS      TEXT,
                      LIBRARY       TEXT,
                      FLAG          TEXT
                      );""")
        print("Table created successfully")
        conn.commit()
        self.conn = conn
        self.insert_count = 0
        self.sql_data = []

    def process_one(self, args):
        reses = []
        apk = args
        apkname = os.path.split(apk)[-1][:-4]

        pkg_name = self.scrapAPK.sha256_pkg_map[apkname]
        metadata = self.scrapAPK.process_one(pkg_name)
        if not metadata:
            return

        summary = metadata['SUMMARY']
        description = metadata['DESCRIPTION']
        normalization = Normalization()
        if normalization.judge_pure_english(description) != "en":
            return
        new_summary = " ".join(normalization.normalize(summary))
        new_desc = " ".join(normalization.normalize(description))

        with open(apk, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                res = {
                    "PIC_NAME": line[0],
                    "IDNAME": line[1],
                    "ICON_TYPE": line[2],
                    "TEXT_ON_ICON": line[3],
                    "APK_SHA256": line[4],
                    "EVENT": line[5],
                    "HANDLER": line[6],
                    "PIC_PATH": line[7],
                    "CODE_BODY": "",
                    "API_LEVEL": "",  # e.g., 27-29
                    "SUMMARY": new_summary,
                    "DESCRIPTION": new_desc,
                    "SCORE": metadata["SCORE"],
                    "INSTALLS": metadata["INSTALLS"],
                    "LIBRARY": "",
                    "FLAG": "1"
                }
                reses.append(res)
        return reses

    def save_result(self, request, reses):
        # if catch exception
        if not reses:
            return

        for res in reses:
            self.lock.acquire()
            self.total_insert += 1

            if self.total_insert % 20 == 0:
                print(self.total_insert)

            row = (res['PIC_NAME'], res['IDNAME'], res['ICON_TYPE'], res['TEXT_ON_ICON'],
                   res['APK_SHA256'], res['EVENT'], res['HANDLER'], res['PIC_PATH'],
                   res['CODE_BODY'], res['API_LEVEL'], res['SUMMARY'], res['DESCRIPTION'],
                   res['SCORE'], res['INSTALLS'], res['LIBRARY'], res['FLAG'])
            if self.insert_count > 400:
                self.sql_data.append(row)
                # sql = """UPDATE DATA SET DEX_MD5 = ? WHERE PATH like ?"""
                sql = """INSERT INTO DATA(PIC_NAME, IDNAME, ICON_TYPE, TEXT_ON_ICON,
                      APK_SHA256, EVENT, HANDLER, PIC_PATH,
                      CODE_BODY, API_LEVEL, SUMMARY, DESCRIPTION,
                      SCORE, INSTALLS, LIBRARY, FLAG)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
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


class Normalization:
    def __init__(self):
        self.english_stopwords = stopwords.words("english")

    def check_lang(self, file):
        count = 0
        with open(file, "r") as fr:
            content = fr.read()
            for char in content:
                if ord(char) > 128:
                    count += 1
        # Non English char / all < 0.1, keep; otherwise, remove
        if 1.0 * count / len(content) < 0.1:
            return True
        else:
            return False

    # lemmatizer
    def lemmatizer(self, tokens):
        wordnet_lemmatizer = WordNetLemmatizer()
        return [wordnet_lemmatizer.lemmatize(item) for item in tokens]

    # stemming
    def stem_tokens(self, tokens):
        stemmer = PorterStemmer()
        return [stemmer.stem(item) for item in tokens]

    '''remove punctuation, lowercase, stem'''

    def judge_pure_english(self, text):
        try:
            lang1 = detect_langs(text)[0]
        except UnicodeDecodeError:
            lang1 = detect_langs(text.decode("utf-8"))[0]
        prob = lang1.prob
        lang = lang1.lang
        if prob > 0.90:
            return lang
        return None

    def normalize(self, text):
        words_cut = word_tokenize(text)
        words_lower = [i.lower() for i in words_cut if len(i) > 3]
        words_clear = []
        for i in words_lower:
            if not self.judge_pure_english(i):
                continue
            if i not in self.english_stopwords and i not in string.punctuation:
                i1 = re.sub('[^a-zA-Z]', '', i)
                words_clear.append(i1)
        return self.stem_tokens(words_clear)


class filterDB:
    def __init__(self, database_db, new_name):
        self.db_name_old = database_db
        self.new_db_name = new_name

    def connect_database(self):
        """
        :param database: filepath of database
        :return: sqlite connection
        """
        conn = sqlite3.connect(self.new_db_name)
        print("Opened database successfully")

        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS DATA
                     (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      PIC_NAME      TEXT    NOT NULL,
                      IDNAME        TEXT    NOT NULL,
                      ICON_TYPE     TEXT    NOT NULL,
                      TEXT_ON_ICON  TEXT,
                      APK_SHA256    TEXT    NOT NULL,
                      EVENT         TEXT,
                      HANDLER       TEXT,
                      PIC_PATH      TEXT,
                      CODE_BODY     TEXT,
                      API_LEVEL     TEXT,
                      SUMMARY       TEXT,
                      DESCRIPTION   TEXT,
                      SCORE         TEXT, 
                      INSTALLS      TEXT,
                      LIBRARY       TEXT,
                      FLAG          TEXT
                      );""")
        print("Table created successfully")
        conn.commit()
        self.conn = conn
        self.insert_count = 0

    def start(self):
        self.read()
        self.new_dict = {}
        for item in self.datas:
            item = list(item)
            sha256 = item[8]
            if sha256 in self.new_dict:
                self.new_dict[sha256].extend(item[-2].split(';'))
            else:
                self.new_dict[sha256] = item[-2].split(';')

        self.connect_database()
        sql = """INSERT INTO DATA(PIC_NAME, IDNAME, ICON_TYPE, TEXT_ON_ICON,
                              APK_SHA256, EVENT, HANDLER, PIC_PATH,
                              CODE_BODY, API_LEVEL, SUMMARY, DESCRIPTION,
                              SCORE, INSTALLS, LIBRARY, FLAG)
                              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        for item in self.datas:
            tmp = list(item)
            if tmp[8] in self.new_dict:
                tmp[-2] = ";".join(self.new_dict[tmp[8]])
                tmp = tuple(tmp[1:])
                cursor = self.conn.cursor()
                cursor.execute(sql, tmp)
                self.conn.commit()

    def close(self):
        self.conn.close()

    def read(self):
        conn = sqlite3.connect(self.db_name_old)
        print("Opened database successfully")
        cu = conn.cursor()
        sql = """SELECT * FROM DATA WHERE LIBRARY != ''"""
        results = cu.execute(sql)
        self.datas = results.fetchall()
        conn.close()


if __name__ == "__main__":
    database = Database(Database_name)
    database.start()
    database.close()

    # f = filterDB(Database_name, New_database_name)
    # f.start()
    # f.close()

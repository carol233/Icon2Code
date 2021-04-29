import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import sqlite3
from common import *
import numpy as np

class Analysis:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)

    def select_query(self):
        cu = self.conn.cursor()

        sql = """select * from data where LIBRARY != '' and FLAG = '2' """

        results = cu.execute(sql)
        tmplist = results.fetchall()
        return tmplist

    def query_icon(self):
        res = {}
        cu = self.conn.cursor()
        sql = """select * from data where LIBRARY != '' and FLAG = '2' """
        results = cu.execute(sql)
        tmplist = results.fetchall()
        for item in tmplist:
            sha256 = item[5]
            if sha256 in res:
                res[sha256] += 1
            else:
                res[sha256] = 1
        return res


def to_percent(temp):
    return ('%.f%%' % (temp * 100))


def draw_api_num():
    box = []
    analysis = Analysis(Database_name)
    results = analysis.select_query()
    for item in results:
        lib = item[15].split(';')
        count = len(lib)
        box.append(count)

    labels = ["#.APIs"]
    print(len(box))
    plt.figure(figsize=(8, 3))  # 设置画布的尺寸
    # vert=False:水平箱线图；showmeans=True：显示均值
    plt.boxplot([box], labels=labels, vert=False, showmeans=True, showfliers=False)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    # plt.xlim((10, 11))

    # plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig("boxplot_api_num.pdf")
    plt.close()


def draw_icon_num():
    box = []
    analysis = Analysis(Database_name)
    results = analysis.query_icon()
    for item in results:
        box.append(results[item])
    labels = ["#.Icons"]

    plt.figure(figsize=(8, 3))  # 设置画布的尺寸
    # vert=False:水平箱线图；showmeans=True：显示均值
    plt.boxplot([box], labels=labels, vert=False, showmeans=True, showfliers=False)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig("boxplot_icon_num.pdf")
    plt.close()


if __name__ == '__main__':
    draw_api_num()
    # draw_icon_num()

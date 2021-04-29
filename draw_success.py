import csv
import os
from common import *
import numpy as np
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def count_successrate(files):
    valid = 0
    num = 0
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                score = float(line[1])
                if score:
                    valid += 1
                num += 1
    return float(valid * 1.0 / (num + 0.0001))

def to_percent(temp, position):
    return '%1.0f'%(100*temp) + '%'


if __name__ == '__main__':

    y_20 = []

    for i in [2]:
        for topnum in range(1, 21):
            start_s = str(i) + "evaluation" + str(topnum) + "_"
            path = "m20res/"
            files = getFileList2(path, start_s, ".csv")
            res = count_successrate(files)
            if i == 2:
                y_20.append(res)

    x_axix = [i for i in range(1, 21)]

    plt.figure(figsize=(8, 4.5))

    plt.bar(x_axix, y_20, color=(0.1, 0.1, 0.1, 0.1), edgecolor='black')

    for a, b in zip(x_axix, y_20):
        plt.text(a, b, '%.2f%%' % (b * 100), ha='center', va='top', rotation=90, fontsize=12)

    plt.xlabel('N value', fontsize=14)
    plt.ylabel('Success rate', fontsize=14)
    plt.xticks(range(1, 21))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    # plt.show()
    #plt.legend()
    plt.savefig("successrate1.pdf")
    plt.close()

#     y_20 = []
#     y_15 = []
#     y_10 = []
#     y_5 = []
#     y_25 = []
#     y_30 = []
#
#     for i in [2,3,4,5,9,10]:
#         for topnum in range(1, 21):
#             start_s = str(i) + "evaluation" + str(topnum) + "_"
#             path = "m20res/"
#             files = getFileList2(path, start_s, ".csv")
#             res = count_successrate(files)
#             if i == 2:
#                 y_20.append(res)
#             if i == 3:
#                 y_15.append(res)
#             if i == 4:
#                 y_10.append(res)
#             if i == 5:
#                 y_5.append(res)
#             if i == 9:
#                 y_25.append(res)
#             if i == 10:
#                 y_30.append(res)
#
#
#     x_axix = [i for i in range(1, 21)]
#
#     plt.figure(figsize=(8, 4.5))
#
#
#     # plt.text(x_axix[0], y_20[0], '%.2f%%' % (y_20[0] * 100), ha='right', va='bottom', rotation=90, fontsize=9)
#     # for a, b in zip(x_axix[1:], y_20[1:]):
#     #     plt.text(a, b, '%.2f%%' % (b * 100), ha='left', va='top', rotation=90, fontsize=9)
#     plt.plot(x_axix, y_30, 'b*-', label='m=30')
#     plt.plot(x_axix, y_25, 'rv-', label='m=25')
#     plt.plot(x_axix, y_20, 'go-', label='m=20')
#     plt.plot(x_axix, y_15, 'm>-', label='m=15')
#     plt.plot(x_axix, y_10, 'c^-', label='m=10')
#     plt.plot(x_axix, y_5, 'y.-', label='m=5')
#
#
#
#     plt.xlabel('N value', fontsize=14)
#     plt.ylabel('Success rate', fontsize=14)
#     plt.xticks(range(1, 21))
#     plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
#     # plt.show()
#     plt.legend()
#     plt.savefig("successrate4.pdf")
#     plt.close()
# ################################################################
#     y_20 = []
#     y_08 = []
#     y_05 = []
#     y_02 = []
#     y_t = []
#
#
#     for i in [2,6,8,11,12]:
#         for topnum in range(1, 21):
#             start_s = str(i) + "evaluation" + str(topnum) + "_"
#             path = "m20res/"
#             files = getFileList2(path, start_s, ".csv")
#             res = count_successrate(files)
#             if i == 2:
#                 y_20.append(res)
#             if i == 6:
#                 y_t.append(res)
#             if i == 8:
#                 y_05.append(res)
#             if i == 11:
#                 y_02.append(res)
#             if i == 12:
#                 y_08.append(res)
#
#     x_axix = [i for i in range(1, 21)]
#
#     plt.figure(figsize=(8, 4.5))
#
#
#     plt.plot(x_axix, y_t, 'm>-', label='(0,1)')
#     plt.plot(x_axix, y_02, 'r<-', label='(0.2,0.8)')
#     plt.plot(x_axix, y_05, 'c.-', label='(0.5,0.5)')
#     plt.plot(x_axix, y_08, 'y*-', label='(0.8,0.2)')
#     plt.plot(x_axix, y_20, 'go-', label='(1,0)')
#
#     # plt.text(x_axix[0], y_20[0], '%.2f%%' % (y_20[0] * 100), ha='right', va='bottom', rotation=90, fontsize=9)
#     # for a, b in zip(x_axix[1:], y_20[1:]):
#     #     plt.text(a, b, '%.2f%%' % (b * 100), ha='left', va='top', rotation=90, fontsize=9)
#
#     plt.xlabel('N value', fontsize=14)
#     plt.ylabel('Success rate', fontsize=14)
#     plt.xticks(range(1, 21))
#     plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
#     # plt.show()
#     plt.legend()
#     plt.savefig("successrate3.pdf")
#     plt.close()

    # y_20 = []
    # y_d = []
    #
    # for i in [2, 7]:
    #     for topnum in range(1, 21):
    #         start_s = str(i) + "evaluation" + str(topnum) + "_"
    #         path = "m20res/"
    #         files = getFileList2(path, start_s, ".csv")
    #         res = count_successrate(files)
    #         if i == 2:
    #             y_20.append(res)
    #         if i == 7:
    #             y_d.append(res)
    #
    # x_axix = [i for i in range(1, 21)]
    #
    # plt.figure(figsize=(8, 4.5))
    # plt.plot(x_axix, y_20, 'go-', label='No Dup.')
    #
    # # plt.text(x_axix[0], y_20[0], '%.2f%%' % (y_20[0] * 100), ha='right', va='bottom', rotation=90, fontsize=9)
    # # for a, b in zip(x_axix[1:], y_20[1:]):
    # #     plt.text(a, b, '%.2f%%' % (b * 100), ha='left', va='top', rotation=90, fontsize=9)
    #
    # plt.plot(x_axix, y_d, 'b^-', label='With Dup.')
    #
    # plt.xlabel('N value', fontsize=14)
    # plt.ylabel('Success rate', fontsize=14)
    # plt.xticks(range(1, 21))
    # plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    # # plt.show()
    # plt.legend()
    # plt.savefig("successrate5.pdf")
    # plt.close()
from matplotlib.ticker import FuncFormatter
import numpy as np
from common import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def get_scores(files):
    precisions = []
    recalls = []
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                precision = round(float(line[1]), 4)
                recall = round(float(line[2]), 4)
                precisions.append(precision)
                recalls.append(recall)
    return precisions, recalls


def get_scores_dic(files):
    precisions = {}
    recalls = {}
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                item = line[0]
                precision = round(float(line[1]), 4)
                recall = round(float(line[2]), 4)
                precisions[item] = precision
                recalls[item] = recall
    return precisions, recalls


def write2file(map, file):
    with open(file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["precision", "recall"])
        for item in map:
            writer.writerow([str(item), str(map[item])])


def draw_boxplot(baseline_p, baseline_r, focus_p, focus_r, matchmaker_p, matchmaker_r):
    plt.figure(figsize=(30, 10))  # 创建画布
    fig, axes = plt.subplots(2, 5)
    ax = axes.flatten()
    titlepre = "Precision"
    titlerec = "Recall"

    for i in range(5):
        if i == 0:
            baseline = "B" + "(" + str(1) + ")"
            matchmaker = "M" + "(" + str(1) + ")"
            focus = "F" + "(" + str(1) + ")"
        else:
            baseline = "B" + "(" + str(i * 5) + ")"
            matchmaker = "M" + "(" + str(i * 5) + ")"
            focus = "F" + "(" + str(i * 5) + ")"
        all_data = {
            matchmaker: matchmaker_p[i],
            focus: focus_p[i],
            baseline: baseline_p[i]
        }

        color = dict(boxes='Black', whiskers='Black',
                     medians='Red', caps='Black')

        columns = [matchmaker, focus, baseline]
        df = pd.DataFrame(all_data, columns=columns)
        if i == 2:
            df.plot.box(title=titlepre, ax=ax[i], color=color, sym="-", rot=45)
        else:
            df.plot.box(title="", ax=ax[i], color=color, sym="-", rot=45)

    for i in range(5, 10):
        if i == 5:
            baseline = "B" + "(" + str(1) + ")"
            matchmaker = "M" + "(" + str(1) + ")"
            focus = "F" + "(" + str(1) + ")"
        else:
            baseline = "B" + "(" + str((i - 5) * 5) + ")"
            matchmaker = "M" + "(" + str((i - 5) * 5) + ")"
            focus = "F" + "(" + str((i - 5) * 5) + ")"
        all_data = {
            matchmaker: matchmaker_r[i - 5],
            focus: focus_r[i - 5],
            baseline: baseline_r[i - 5]
        }
        color = dict(boxes='Black', whiskers='Black',
                     medians='Red', caps='Black')

        columns = [matchmaker, focus, baseline]
        df = pd.DataFrame(all_data, columns=columns)
        if i == 7:
            df.plot.box(title=titlerec, ax=ax[i], color=color, sym="-", rot=45)
        else:
            df.plot.box(title="", ax=ax[i], color=color, sym="-", rot=45)

    plt.tight_layout()
    plt.savefig("boxplot_all_4.pdf")
    plt.close()


def draw_single_boxplot(rank_p, rank_r, matchmaker_p, matchmaker_r):
    plt.figure(figsize=(30, 10))  # 创建画布
    fig, axes = plt.subplots(2, 5)
    ax = axes.flatten()
    titlepre = "Precision"
    titlerec = "Recall"

    for i in range(5):
        if i == 0:
            rank = "Ordered" + "(" + str(1) + ")"
            matchmaker = "Random" + "(" + str(1) + ")"

        else:
            rank = "Ordered" + "(" + str(i * 5) + ")"
            matchmaker = "Random" + "(" + str(i * 5) + ")"

        len1 = len(rank_p[i])
        len2 = len(matchmaker_p[i])
        leng = min(len1, len2)

        all_data = {
            matchmaker: matchmaker_p[i][:leng],
            rank: rank_p[i][:leng]
        }

        color = dict(boxes='Black', whiskers='Black',
                     medians='Red', caps='Black')

        columns = [matchmaker, rank]
        df = pd.DataFrame(all_data, columns=columns)
        if i == 2:
            df.plot.box(title=titlepre, ax=ax[i], color=color, sym="-", rot=45)
        else:
            df.plot.box(title="", ax=ax[i], color=color, sym="-", rot=45)

    for i in range(5, 10):
        if i == 5:
            rank = "Ordered" + "(" + str(1) + ")"
            matchmaker = "Random" + "(" + str(1) + ")"

        else:
            rank = "Ordered" + "(" + str((i - 5) * 5) + ")"
            matchmaker = "Random" + "(" + str((i - 5) * 5) + ")"

        len1 = len(rank_r[i-5])
        len2 = len(matchmaker_r[i-5])
        leng = min(len1, len2)

        all_data = {
            matchmaker: matchmaker_r[i-5][:leng],
            rank: rank_r[i-5][:leng]
        }

        color = dict(boxes='Black', whiskers='Black',
                     medians='Red', caps='Black')

        columns = [matchmaker, rank]
        df = pd.DataFrame(all_data, columns=columns)
        if i == 7:
            df.plot.box(title=titlerec, ax=ax[i], color=color, sym="-", rot=45)
        else:
            df.plot.box(title="", ax=ax[i], color=color, sym="-", rot=45)

    plt.tight_layout()
    plt.savefig("boxplot_rank.pdf")
    plt.close()


def draw_boxplot3(matchmaker_p, matchmaker_r, lst206_p, lst206_r, lst1012_p, lst1012_r):
    plt.figure(figsize=(30, 10))  # 创建画布
    fig, axes = plt.subplots(2, 5)
    ax = axes.flatten()
    titlepre = "Precision"
    titlerec = "Recall"

    for i in range(5):
        if i == 0:
            lst206 = "(20,6)" + "(" + str(1) + ")"
            matchmaker = "(10,6)" + "(" + str(1) + ")"
            lst1012 = "(10,12)" + "(" + str(1) + ")"
        else:
            lst206 = "(20,6)" + "(" + str(i * 5) + ")"
            matchmaker = "(10,6)" + "(" + str(i * 5) + ")"
            lst1012 = "(10,12)" + "(" + str(i * 5) + ")"
        all_data = {
            matchmaker: matchmaker_p[i],
            lst206: lst206_p[i],
            lst1012: lst1012_p[i]
        }

        color = dict(boxes='Black', whiskers='Black',
                     medians='Red', caps='Black')

        columns = [matchmaker, lst206, lst1012]
        df = pd.DataFrame(all_data, columns=columns)
        if i == 2:
            df.plot.box(title=titlepre, ax=ax[i], color=color, sym="-", rot=45)
        else:
            df.plot.box(title="", ax=ax[i], color=color, sym="-", rot=45)

    for i in range(5, 10):
        if i == 5:
            lst206 = "(20,6)" + "(" + str(1) + ")"
            matchmaker = "(10,6)" + "(" + str(1) + ")"
            lst1012 = "(10,12)" + "(" + str(1) + ")"
        else:
            lst206 = "(20,6)" + "(" + str((i - 5) * 5) + ")"
            matchmaker = "(10,6)" + "(" + str((i - 5) * 5) + ")"
            lst1012 = "(10,12)" + "(" + str((i - 5) * 5) + ")"
        all_data = {
            matchmaker: matchmaker_r[i - 5],
            lst206: lst206_r[i - 5],
            lst1012: lst1012_r[i - 5]
        }
        color = dict(boxes='Black', whiskers='Black',
                     medians='Red', caps='Black')

        columns = [matchmaker, lst206, lst1012]
        df = pd.DataFrame(all_data, columns=columns)
        if i == 7:
            df.plot.box(title=titlerec, ax=ax[i], color=color, sym="-", rot=45)
        else:
            df.plot.box(title="", ax=ax[i], color=color, sym="-", rot=45)

    plt.tight_layout()
    plt.savefig("boxplot_xy_all_4.pdf")
    plt.close()


def to_percent(temp, position):
    return '%1.0f'%(100*temp) + '%'


def draw_boxplot111(ps, rs, x):
    labels = [str(i) for i in x]

    plt.figure(figsize=(8, 3))  # 设置画布的尺寸
    # vert=False:水平箱线图；showmeans=True：显示均值
    plt.boxplot(ps, labels=labels, vert=True, showmeans=True, showfliers=False)
    # plt.xticks(fontsize=14)
    # plt.yticks(fontsize=14)
    plt.xlabel('N value', fontsize=14)
    plt.ylabel('Precision', fontsize=14)

    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig("boxplot_precision.pdf")
    plt.close()

    plt.figure(figsize=(8, 3))  # 设置画布的尺寸
    # vert=False:水平箱线图；showmeans=True：显示均值
    plt.boxplot(rs, labels=labels, vert=True, showmeans=True, showfliers=False)
    # plt.xticks(fontsize=12)
    # plt.yticks(fontsize=12)
    plt.xlabel('N value', fontsize=14)
    plt.ylabel('Recall', fontsize=14)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig("boxplot_recall.pdf")
    plt.close()


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)


def draw_boxplot222(p1, r1, p2, r2, p3, r3, p4, r4, p5, r5, p6, r6, x):
    labels = [str(i) for i in x]

    plt.figure(figsize=(16, 3))  # 设置画布的尺寸

    bp1 = plt.boxplot(p1, positions=np.array(range(len(p1))) * 4.0 - 1.5, sym='', widths=0.4)
    bp2 = plt.boxplot(p2, positions=np.array(range(len(p2))) * 4.0 - 0.9, sym='', widths=0.4)
    bp3 = plt.boxplot(p3, positions=np.array(range(len(p3))) * 4.0 - 0.3, sym='', widths=0.4)
    bp4 = plt.boxplot(p4, positions=np.array(range(len(p4))) * 4.0 + 0.3, sym='', widths=0.4)
    bp5 = plt.boxplot(p5, positions=np.array(range(len(p5))) * 4.0 + 0.9, sym='', widths=0.4)
    bp6 = plt.boxplot(p6, positions=np.array(range(len(p6))) * 4.0 + 1.5, sym='', widths=0.4)

    set_box_color(bp1, 'g')  # colors are from http://colorbrewer2.org/
    set_box_color(bp2, 'm')
    set_box_color(bp3, 'k')  # colors are from http://colorbrewer2.org/
    set_box_color(bp4, 'c')
    set_box_color(bp5, 'r')
    set_box_color(bp6, 'gray')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='g', label='m=30')
    plt.plot([], c='m', label='m=25')
    plt.plot([], c='k', label='m=20')
    plt.plot([], c='c', label='m=15')
    plt.plot([], c='r', label='m=10')
    plt.plot([], c='gray', label='m=5')

    plt.legend(loc='upper right')

    plt.xticks(range(0, len(labels) * 4, 4), labels)
    plt.xlim(-4, len(labels) * 4)

    plt.xlabel('N value', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig('boxplot_rq2_precision.pdf')
    plt.close()


    ########################

    plt.figure(figsize=(16, 3))  # 设置画布的尺寸

    bp1 = plt.boxplot(r1, positions=np.array(range(len(r1))) * 4.0 - 1.5, sym='', widths=0.4)
    bp2 = plt.boxplot(r2, positions=np.array(range(len(r2))) * 4.0 - 0.9, sym='', widths=0.4)
    bp3 = plt.boxplot(r3, positions=np.array(range(len(r3))) * 4.0 - 0.3, sym='', widths=0.4)
    bp4 = plt.boxplot(r4, positions=np.array(range(len(r4))) * 4.0 + 0.3, sym='', widths=0.4)
    bp5 = plt.boxplot(r5, positions=np.array(range(len(r5))) * 4.0 + 0.9, sym='', widths=0.4)
    bp6 = plt.boxplot(r6, positions=np.array(range(len(r6))) * 4.0 + 1.5, sym='', widths=0.4)

    set_box_color(bp1, 'g')  # colors are from http://colorbrewer2.org/
    set_box_color(bp2, 'm')
    set_box_color(bp3, 'k')  # colors are from http://colorbrewer2.org/
    set_box_color(bp4, 'c')
    set_box_color(bp5, 'r')
    set_box_color(bp6, 'gray')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='g', label='m=30')
    plt.plot([], c='m', label='m=25')
    plt.plot([], c='k', label='m=20')
    plt.plot([], c='c', label='m=15')
    plt.plot([], c='r', label='m=10')
    plt.plot([], c='gray', label='m=5')
    plt.legend(loc='upper right')

    plt.xticks(range(0, len(labels) * 4, 4), labels)
    plt.xlim(-4, len(labels) * 4)

    plt.xlabel('N value', fontsize=12)
    plt.ylabel('Recall', fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig('boxplot_rq2_recall.pdf')
    plt.close()


def draw_boxplot333(p1, r1, p2, r2, p3, r3, p4, r4, p5, r5, x):
    labels = [str(i) for i in x]

    c1 = 'brown'
    c2 = 'hotpink'
    c3 = 'gray'
    c4 = 'lightseagreen'
    c5 = 'dodgerblue'

    plt.figure(figsize=(16, 3))  # 设置画布的尺寸

    bp1 = plt.boxplot(p1, positions=np.array(range(len(p1))) * 4.0 - 1.4, sym='', widths=0.5)
    bp2 = plt.boxplot(p2, positions=np.array(range(len(p2))) * 4.0 - 0.7, sym='', widths=0.5)
    bp3 = plt.boxplot(p3, positions=np.array(range(len(p3))) * 4.0, sym='', widths=0.5)
    bp4 = plt.boxplot(p4, positions=np.array(range(len(p4))) * 4.0 + 0.7, sym='', widths=0.5)
    bp5 = plt.boxplot(p5, positions=np.array(range(len(p5))) * 4.0 + 1.4, sym='', widths=0.5)

    set_box_color(bp1, c1)  # colors are from http://colorbrewer2.org/
    set_box_color(bp2, c2)
    set_box_color(bp3, c3)
    set_box_color(bp4, c4)
    set_box_color(bp5, c5)


    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c=c1, label='(1,0)')
    plt.plot([], c=c2, label='(0.8,0.2)')
    plt.plot([], c=c3, label='(0.5,0.5)')
    plt.plot([], c=c4, label='(0.2,0.8)')
    plt.plot([], c=c5, label='(0,1)')
    plt.legend(loc='upper right')

    plt.xticks(range(0, len(labels) * 4, 4), labels)
    plt.xlim(-4, len(labels) * 4)

    plt.xlabel('N value', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig('boxplot_rq3_precision.pdf')
    plt.close()


    plt.figure(figsize=(16, 3))  # 设置画布的尺寸

    bp1 = plt.boxplot(r1, positions=np.array(range(len(r1))) * 4.0 - 1.4, sym='', widths=0.5)
    bp2 = plt.boxplot(r2, positions=np.array(range(len(r2))) * 4.0 - 0.7, sym='', widths=0.5)
    bp3 = plt.boxplot(r3, positions=np.array(range(len(r3))) * 4.0, sym='', widths=0.5)
    bp4 = plt.boxplot(r4, positions=np.array(range(len(r4))) * 4.0 + 0.7, sym='', widths=0.5)
    bp5 = plt.boxplot(r5, positions=np.array(range(len(r5))) * 4.0 + 1.4, sym='', widths=0.5)

    set_box_color(bp1, c1)  # colors are from http://colorbrewer2.org/
    set_box_color(bp2, c2)
    set_box_color(bp3, c3)
    set_box_color(bp4, c4)
    set_box_color(bp5, c5)

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c=c1, label='(1,0)')
    plt.plot([], c=c2, label='(0.8,0.2)')
    plt.plot([], c=c3, label='(0.5,0.5)')
    plt.plot([], c=c4, label='(0.2,0.8)')
    plt.plot([], c=c5, label='(0,1)')
    plt.legend(loc='upper right')

    plt.xticks(range(0, len(labels) * 4, 4), labels)
    plt.xlim(-4, len(labels) * 4)

    plt.xlabel('N value', fontsize=12)
    plt.ylabel('Recall', fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig('boxplot_rq3_recall.pdf')
    plt.close()


def draw_boxplot444(p1, r1, p2, r2,  x):
    labels = [str(i) for i in x]


    plt.figure(figsize=(8, 3))  # 设置画布的尺寸

    bp1 = plt.boxplot(p1, positions=np.array(range(len(p1))) * 4.0 - 0.8, sym='', widths=0.8)
    bp2 = plt.boxplot(p2, positions=np.array(range(len(p2))) * 4.0 + 0.8, sym='', widths=0.8)

    set_box_color(bp1, 'g')  # colors are from http://colorbrewer2.org/
    set_box_color(bp2, 'b')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='g', label='No Dup.')
    plt.plot([], c='b', label='With Dup.')
    plt.legend(loc='upper right')

    plt.xticks(range(0, len(labels) * 4, 4), labels)
    plt.xlim(-4, len(labels) * 4)

    plt.xlabel('N value', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig('boxplot_rq5_precision.pdf')
    plt.close()


    plt.figure(figsize=(8, 3))  # 设置画布的尺寸

    bp1 = plt.boxplot(r1, positions=np.array(range(len(r1))) * 4.0 - 0.8, sym='', widths=0.8)
    bp2 = plt.boxplot(r2, positions=np.array(range(len(r2))) * 4.0 + 0.8, sym='', widths=0.8)

    set_box_color(bp1, 'g')  # colors are from http://colorbrewer2.org/
    set_box_color(bp2, 'b')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='g', label='No Dup.')
    plt.plot([], c='b', label='With Dup.')
    plt.legend(loc='upper right')

    plt.xticks(range(0, len(labels) * 4, 4), labels)
    plt.xlim(-4, len(labels) * 4)

    plt.xlabel('N value', fontsize=12)
    plt.ylabel('Recall', fontsize=12)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.tight_layout()
    plt.savefig('boxplot_rq5_recall.pdf')
    plt.close()


if __name__ == '__main__':

    path = "m20res/"

    p_20 = []
    r_20 = []
    p_15 = []
    r_15 = []
    p_10 = []
    r_10 = []
    p_5 = []
    r_5 = []
    p_25 = []
    r_25 = []
    p_30 = []
    r_30 = []

    for i in [2,3,4,5,9,10]:
        for topnum in range(1, 21):
            start_s = str(i) + "evaluation" + str(topnum) + "_"
            path = "m20res/"
            files = getFileList2(path, start_s, ".csv")
            p_t, r_t = get_scores(files)

            if i == 2:
                p_20.append(p_t)
                r_20.append(r_t)
            elif i == 3:
                p_15.append(p_t)
                r_15.append(r_t)
            elif i == 4:
                p_10.append(p_t)
                r_10.append(r_t)
            elif i == 5:
                p_5.append(p_t)
                r_5.append(r_t)
            elif i == 9:
                p_25.append(p_t)
                r_25.append(r_t)
            elif i == 10:
                p_30.append(p_t)
                r_30.append(r_t)


    x = [i for i in range(1, 21)]

    draw_boxplot222(p_30,r_30,p_25,r_25,p_20,r_20, p_15, r_15, p_10, r_10, p_5, r_5, x)

################################################
    path = "m20res/"

    p_20 = []
    r_20 = []
    p_t = []
    r_t = []
    p_05 = []
    r_05 = []
    p_02 = []
    r_02 = []
    p_08 = []
    r_08 = []

    for i in [2,6,8,11,12]:
        for topnum in range(1, 21):
            start_s = str(i) + "evaluation" + str(topnum) + "_"
            path = "m20res/"
            files = getFileList2(path, start_s, ".csv")
            p, r = get_scores(files)

            if i == 2:
                p_20.append(p)
                r_20.append(r)
            elif i == 6:
                p_t.append(p)
                r_t.append(r)
            elif i == 8:
                p_05.append(p)
                r_05.append(r)
            elif i == 11:
                p_02.append(p)
                r_02.append(r)
            elif i == 12:
                p_08.append(p)
                r_08.append(r)

    x = [i for i in range(1, 21)]

    draw_boxplot333(p_20, r_20, p_08, r_08, p_05, r_05, p_02, r_02, p_t, r_t, x)
################################################################
    # path = "m20res/"
    #
    # p_20 = []
    # r_20 = []
    # p_d = []
    # r_d = []
    #
    #
    # for i in [2, 7]:
    #     for topnum in range(1, 21):
    #         start_s = str(i) + "evaluation" + str(topnum) + "_"
    #         path = "m20res/"
    #         files = getFileList2(path, start_s, ".csv")
    #         p, r = get_scores(files)
    #
    #         if i == 2:
    #             p_20.append(p)
    #             r_20.append(r)
    #         elif i == 7:
    #             p_d.append(p)
    #             r_d.append(r)
    #
    # x = [i for i in range(1, 21)]
    #
    # draw_boxplot444(p_20, r_20, p_d, r_d, x)










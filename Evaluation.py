import sys

from common import *

class Evaluation:
    def __init__(self, OPTIONS, datas, n, name_num):
        self.OPTIONS = OPTIONS
        self.datas = datas
        self.n = n
        self.name_num = name_num

    def start(self):
        testingIcons = []
        evaluations = []
        files = getFileList(self.OPTIONS.output, ".csv")
        for file in files:
            testingIcons.append(int(os.path.split(file)[-1][:-4]))
        for testIcon in testingIcons:
            if not self.getGroundTruthLibs(testIcon):
                continue
            GT_set = set(self.getGroundTruthLibs(testIcon))
            pre_lst = self.getPrediction_lst(testIcon, self.n)
            if len(GT_set) < self.n or len(pre_lst) < self.n:
                continue
            intersections = GT_set.intersection(set(pre_lst))
            precision = 1.0 * len(intersections) / self.n
            recall = 1.0 * len(intersections) / len(GT_set)
            evaluations.append([testIcon, precision, recall])
        self.record_acc(str(self.name_num) + "evaluation", evaluations)

    def getGroundTruthLibs(self, testingIcon):
        if testingIcon not in self.datas:
            return None
        line = self.datas[testingIcon]
        library = line[-2].split(";")
        return library

    def getPrediction_lst(self, testingIcon, n):
        res = []
        filename = os.path.join(self.OPTIONS.output, str(testingIcon) + ".csv")
        if not os.path.exists(filename):
            return None
        with open(filename, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                if reader.line_num <= n:
                    mi = line[0].strip("\" ")
                    res.append(mi)
        return res

    def record_acc(self, outputpath, evaluations):
        dataset = os.path.split(self.OPTIONS.input)[-1][:-4]
        with open(outputpath + str(self.n) + "_" + dataset + ".csv", "w", newline="") as fw:
            writer = csv.writer(fw)
            for item in evaluations:
                writer.writerow([item[0], round(item[1], 6), round(item[2], 6)])


def count_precision(files):
    all = 0.0
    num = 0
    for file in files:
        print(file)
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                score = float(line[1])
                all += score
                num += 1
    print("precision: " + str(all / num))


def count_recall(files):
    all = 0.0
    num = 0
    for file in files:
        with open(file, "r") as fr:
            reader = csv.reader(fr)
            for line in reader:
                score = float(line[2])
                all += score
                num += 1
    print("recall: " + str(all / num))


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
    print("valid samples: " + str(num))
    print("success rate: " + str(valid / num))


if __name__ == '__main__':
    startss = str(sys.argv[1])
    topnum = str(sys.argv[2])

    start_s = startss + "evaluation"
    start_s = start_s + topnum + "_"

    # path = os.path.abspath(os.path.dirname(os.getcwd()))
    path = os.getcwd()
    files = getFileList2(path, start_s, ".csv")

    count_precision(files)
    count_recall(files)
    count_successrate(files)

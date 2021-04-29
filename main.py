import sys
import argparse
import time

from common import *
from TextQueryRecommendation import TextQueryRecommendation
from IconQueryRecommendation import IconQueryRecommendation
from CombinationRecommendation import CombinationRecommendation
from DataReader import DataReader
from Evaluation import Evaluation

Input_path = os.path.join(Dataset_split_path, "2.txt")
Database_path = Database_name
# Database_path = New_database_name
Output_path = "results/Output0"


def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-i", "--input", default=Input_path, help="Path of the input projects.")
    parser.add_argument("-data", "--database", default=Database_path, help="Database.")
    parser.add_argument("-o", "--output", default=Output_path, help="Path of the outputs.")
    parser.add_argument("-s", "--switch", default=1, help="If use C value.")

    parser.add_argument("-a", "--android_jars", default="/home/yanjie/android-sdk-linux/platforms",
                        help="Path of the dir of android jars.")
    parser.add_argument("-p", "--aapt", default="/home/yanjie/android-sdk-linux/build-tools/30.0.0-preview/aapt",
                        help="Path of aapt.")

    parser.add_argument("-m", "--maxjob", type=int, default=20, help="Max job of threadpools.")
    options = parser.parse_args(args)
    return options


class Runner:
    def __init__(self, OPTIONS):
        self.OPTIONS = OPTIONS

    def start(self):
        name_num = 2
        tmp = self.OPTIONS.output
        self.OPTIONS.output = tmp.split("/")[0] + str(name_num) + "/" + tmp.split("/")[1]
        print(self.OPTIONS.output)
        check_and_mk_dir("results" + str(name_num))
        check_and_mk_dir(self.OPTIONS.output)
        dataReader = DataReader(Database_name)
        self.datas = dataReader.query_all()

        start_time = time.clock()

        # recom = TextQueryRecommendation(OPTIONS, self.datas, 20, 1, 0.33, 0.33, 0.33, 0.5, 0.5, 0, 1)
        recom = IconQueryRecommendation(OPTIONS, self.datas, 20, 1, 0.5, 0.5, 0, 1)
        # recom = CombinationRecommendation(OPTIONS, self.datas, 20, 1, 0.8, 0.2, 0.5, 0.5, 0, 1)
        recom.start()

        # end = time.clock()
        # running_time = end - start_time
        #
        # with open("runtime" + str(name_num) + ".txt", "a+") as fw:
        #     fw.write(str(running_time) + "\n")
        #
        # print("[+] Start evaluation.")
        # for i in range(1, 21):
        #     evaluation = Evaluation(self.OPTIONS, self.datas, i, name_num)
        #     evaluation.start()
        # print("[+] Evaluation done.")


if __name__ == '__main__':
    OPTIONS = getOptions()
    Runner(OPTIONS).start()

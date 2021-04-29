import re
from random import shuffle

import numpy as np
from common import *
from SimCounter import SimCounter
from DataReader import DataReader


class CombinationRecommendation:
    testingIcons = {}
    neighbours = []
    listOfLibs = []
    numOfRows = 0
    numOfCols = 0

    def __init__(self, OPTIONS, datas, numOfNeighbours, img_w, text_w, min_libs, p, q, if_C, if_apk):
        self.OPTIONS = OPTIONS
        self.numOfNeighbours = numOfNeighbours
        self.min_libs = min_libs
        self.datas = datas
        self.p = p
        self.q = q
        self.img_w = img_w
        self.text_w = text_w
        self.if_C = if_C
        self.if_apk = if_apk

    def clear_pre(self):
        self.neighbours = []
        self.listOfLibs = []
        self.numOfRows = 0
        self.numOfCols = 0

    # Recommend new invocations for every testing project using the
    # collaborative-filtering technique

    def start(self):
        testingIcons = self.getTestingIcons()
        for testingIcon in testingIcons:
            self.clear_pre()
            recommendations = {}  # {str: float}

            if os.path.exists(os.path.join(self.OPTIONS.output, str(testingIcon) + ".csv")):
                continue

            # {str: float}
            topnSim = self.getSimilarityScores(testingIcon, self.numOfNeighbours, self.min_libs, testingIcons)
            if not topnSim:
                continue

            print(testingIcon)
            neighbour_list = [item for item in topnSim]
            matrix = self.buildUserItemContextMatrix(neighbour_list)

            # Initial
            ratings = [0.0] * self.numOfCols

            # For every '?' cell (-1.0), compute a rating

            for k in range(self.numOfCols):
                if matrix[self.numOfRows - 1][k] == -1:
                    totalSim = 0.0
                    # Iterate over the top-n most similar methods
                    for j in range(self.numOfRows - 1):
                        neighbour_name = neighbour_list[j]
                        # Compute the average rating of the method declaration
                        avgIconRating = 0.0
                        for m in range(self.numOfCols):
                            avgIconRating += matrix[j][m]
                        avgIconRating /= self.numOfCols

                        if matrix[j][k]:
                            if self.if_C:
                                C_value = self.calculate_C(testingIcon, neighbour_name, self.p, self.q)
                                val = C_value * matrix[j][k]
                            else:
                                val = matrix[j][k]
                        else:
                            val = 0
                        IconSim = topnSim[neighbour_name]
                        totalSim += IconSim
                        ratings[k] += (val - avgIconRating) * IconSim

                    if totalSim:
                        ratings[k] /= totalSim
                    activeMDrating = 0.8
                    ratings[k] += activeMDrating
                    library = self.listOfLibs[k]
                    recommendations[library] = ratings[k]

            recSortedList = dict2sortedlist(recommendations)
            writeScores(self.OPTIONS.output, testingIcon, recSortedList[:20])

    def calculate_C(self, testingIcon, neighbour_name, p, q):
        a = self.datas[testingIcon]
        b = self.datas[neighbour_name]

        SUMMARY_INDEX = 11
        DESCRIPTION_INDEX = 12
        SCORE_INDEX = 13
        INSTALLS_INDEX = 14

        simCounter = SimCounter()
        score_summary = simCounter.cosine_sim(a[SUMMARY_INDEX], b[SUMMARY_INDEX])
        score_description = simCounter.cosine_sim(a[DESCRIPTION_INDEX], b[DESCRIPTION_INDEX])

        C_value = p * score_summary + q * score_description

        return C_value

    def buildUserItemContextMatrix(self, neighbour_list):
        # list
        allLibs = set()
        allData = {}
        for neighbour in neighbour_list:
            b = self.datas[neighbour]
            libs = b[-2].split(";")
            allLibs = allLibs.union(libs)
            allData[neighbour] = libs

        self.listOfLibs = list(allLibs)
        self.numOfRows = len(neighbour_list) + 1
        self.numOfCols = len(allLibs)

        # Populate all cells in the user-item-context ratings matrix using 1s and 0s
        matrix = np.zeros([self.numOfRows, self.numOfCols], dtype=np.int)

        for j in range(self.numOfRows):
            for k in range(self.numOfCols):
                if j != self.numOfRows - 1:
                    libs = allData[neighbour_list[j]]
                    currentLib = self.listOfLibs[k]
                    if currentLib in libs:
                        matrix[j][k] = 1
                else:
                    matrix[j][k] = -1

        return matrix

    def getSimilarityScores(self, testingIcon, numOfNeighbours, min_libs, testingIcons):

        score_dict = {}
        a = self.datas[testingIcon]
        sha256_a = a[5]
        dataReader = DataReader(Database_name)
        filtering_res = dataReader.query_detail(sha256_a, a[3], a[10], a[6], testingIcons, self.if_apk)
        for item in filtering_res:
            b = self.datas[item]
            sha256_b = b[5]
            libs = b[-2].split(";")
            if len(libs) < min_libs:
                continue
            # calculate the simScore of testingIcon
            simCounter = SimCounter()
            score1 = simCounter.edit_distance(a[1], b[1])
            score2 = simCounter.edit_distance(a[2], b[2])
            score3 = simCounter.edit_distance(a[4], b[4])
            text_score = 0.33 * score1 + 0.33 * score2 + 0.33 * score3
            imgae_score = simCounter.image_similarity_score(a[8], sha256_a, b[8], sha256_b)
            score_dict[item] = self.text_w * text_score + self.img_w * imgae_score
        score_lst = dict2sortedlist(score_dict)[:numOfNeighbours]
        topn = {}
        flag = 0
        if len(score_lst) >= numOfNeighbours:
            for item in score_lst:
                if item[1]: flag = 1
                topn[item[0]] = item[1]
            if flag:
                return topn
            else:
                return None
        else:
            return None


    def getTestingIcons(self):
        res = []
        input_path = self.OPTIONS.input
        with open(input_path, "r") as fr:
            lines = fr.readlines()
            for line in lines:
                res.append(int(line))
        shuffle(res)
        return res

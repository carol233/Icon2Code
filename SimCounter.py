import Levenshtein
from fuzzywuzzy import fuzz
from common import *
from sklearn.feature_extraction.text import TfidfVectorizer
from ImageSimCalculator import *


class SimCounter:

    def edit_distance(self, a, b):
        if not a or not b or a == "@null" or b == "@null":
            return 0
        return Levenshtein.ratio(a, b)

    def jaro_winkler_distance(self, a, b):
        if not a or not b:
            return 0
        return Levenshtein.jaro_winkler(a, b)

    def jaro_distance(self, a, b):
        if not a or not b:
            return 0
        return Levenshtein.jaro(a, b)

    def fuzzwuzzy(self, a, b):
        if not a or not b:
            return 0
        return fuzz.ratio(a, b)

    def cosine_sim(self, text1, text2):
        if not text1 or not text2:
            return 0
        vectorizer = TfidfVectorizer(input='content', max_features=2000, min_df=1)
        try:
            tfidf = vectorizer.fit_transform([text1, text2])
            return round((tfidf * tfidf.T).A[0, 1], 6)
        except ValueError:
            print(text1, text2)
            return 0

    def image_similarity_score(self, path1, hash1, path2, hash2):
        tmp1 = path1.split(';')
        tmp2 = path2.split(';')

        if len(tmp1) == 1:
            p1 = get_pic_path(path1, hash1)
        elif len(tmp1) > 1:
            p1 = get_pic_path(tmp1[0], hash1)
        else:
            return 0

        if len(tmp2) == 1:
            p2 = get_pic_path(path2, hash2)
        elif len(tmp2) > 1:
            p2 = get_pic_path(tmp2[0], hash2)
        else:
            return 0

        if not os.path.exists(p1) or not os.path.exists(p2):
            print("img not exist!")
            return 0

        # 融合相似度阈值
        threshold1 = 0.85
        kk = self.calc_image_similarity(p1, p2, threshold1)
        print(kk)
        return kk

    def calc_image_similarity(self, img1_path, img2_path, threshold1):
        similary_ORB = float(ORB_img_similarity(img1_path, img2_path))
        similary_phash = float(phash_img_similarity(img1_path, img2_path))
        similary_hist = float(calc_similar_by_path(img1_path, img2_path))
        # 如果三种算法的相似度最大的那个大于0.85，则相似度取最大，否则，取最小。
        max_three_similarity = max(similary_ORB, similary_phash, similary_hist)
        min_three_similarity = min(similary_ORB, similary_phash, similary_hist)
        if max_three_similarity > threshold1:
            result = max_three_similarity
        else:
            result = min_three_similarity

        return round(result, 4)





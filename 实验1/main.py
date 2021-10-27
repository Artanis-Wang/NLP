import word2vec
import jieba
from collections import Counter


# 加1平滑法
def add1(cnt1: Counter, cnt2: Counter, testStr: str):
    len1 = len(cnt1)
    p = 1
    strList = jieba.lcut(testStr)
    strList.insert(0, "BOS")
    strList.insert(len(strList), "EOS")
    for i in range(len(strList) - 1):
        if i not in cnt1.keys(): # 如果语句中某个词没在词表中出现过，也即没在语料库中出现过，那这句话的概率直接为0。
            tempP = 0
        else:
            bigamyStr = strList[i] + strList[i + 1]
            tempP = (1 + cnt2[bigamyStr]) / (cnt1[strList[i]] + len1 * len1)
        p = p * tempP
    return p


# 2元语法的kneser_ney平滑法
def kneser_ney(cnt1: Counter, cnt2: Counter, dict1: dict, dict2: dict, testStr: str):
    len1 = len(cnt1)
    len2 = len(cnt2)
    strList = jieba.lcut(testStr)
    strList.insert(0, "BOS")
    strList.insert(len(strList), "EOS")
    D = 0.6  # D应该大于0，小于1，这里设置为0。6
    p = 1
    for i in range(len(strList) - 1):
        char1 = strList[i]
        char2 = strList[i + 1]
        if char1 in dict1.keys():  # 计算以char1开头的两个词的种数，也即书上94页的 N1+(wi *)
            lenTemp1 = len(dict1[char1])
        else:
            lenTemp1 = 0
        if char2 in dict2.keys():  # 计算以char1结尾的两个词的种数，也即书上95页的 N1+(* wi)
            lenTemp2 = len(dict2[char2])
        else:
            lenTemp2 = 0
        # 因为这里是2元语法所以无需递归
        tempP = (max(cnt1[char1] - D, 0) / len1) + (D / len1) * lenTemp1 * (lenTemp2 / len2)
        p = p * tempP
        # 一下代码仅用于调试
        # print(
        #     f"i = {i}, char1 = {char1}, char2 = {char2}, cnt1[{char1}] = {cnt1[char1]}, cnt2[{char2}] = {cnt2[char2]}")
        # print(f"len_dic1[{char1}] = {lenTemp1}, len_dic2[{char2}] = {lenTemp2}")
        # print(f"p = {p},  tempP = {tempP}", end="\n\n")
    return p


def show(testStr, cnt1: Counter, cnt2: Counter, dic1: dict, dic2: dict):
    for tempStr in testStr:
        p1 = add1(cnt1, cnt2, tempStr)
        p2 = kneser_ney(cnt1, cnt2, dic1, dic2, tempStr)
        print(f"预测语句: {tempStr}")
        print(f"使用 加1 平滑法计算出的概率为:{p1}")
        print(f"使用 kneser_ney 平滑法计算出的概率为:{p2}", end="\n\n")


def main(testStr):
    f = open("data.txt", "r", encoding="utf-8")
    # 记录单个词出现的频数
    cnt1 = Counter()
    # 记录连续两个词出现的频数
    cnt2 = Counter()
    # 记录以特定字符开头的字符的种数
    dic1 = dict()
    # 记录以特定字符结尾的字符的种数
    dic2 = dict()
    for line in f.readlines():
        words = line.split()
        temp1 = len(words)
        for i in range(temp1):
            cnt1[words[i]] += 1  # 记录words[i]出现的次数
            if i > 0:
                if words[i] not in dic2.keys():
                    dic2[words[i]] = [words[i - 1]]  # 记录以wordfgyyy[i]结尾的两个词的种类数量
                else:
                    if words[i - 1] not in dic2[words[i]]:
                        dic2[words[i]].append(words[i - 1])
            if i != temp1 - 1:
                cnt2[words[i] + words[i + 1]] += 1
                if words[i] not in dic1.keys():  # 记录以words[i]开头的两个词的种类数量
                    dic1[words[i]] = [words[i + 1]]
                else:
                    if words[i + 1] not in dic1[words[i]]:
                        dic1[words[i]].append(words[i + 1])
    f.close()
    for key in cnt1.keys():
        jieba.add_word(key)
    show(testStr, cnt1, cnt2, dic1, dic2)


if __name__ == '__main__':
    testStr = ["我和我的祖国", "中华人民共和国", "爱我中华", "坚持一国两制"]  # 测试语料
    main(testStr)

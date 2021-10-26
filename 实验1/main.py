import word2vec
import jieba
from collections import Counter



def add1(cnt1: Counter, cnt2: Counter, testStr: str):
    len1 = len(cnt1)
    p = 1
    strList = jieba.lcut(testStr)
    strList.insert(0, "BOS")
    strList.insert(len(strList), "EOS")
    print(f"strList的长度为{len(strList)}")
    for i in range(len(strList) - 1):
        bigamyStr = strList[i] + strList[i + 1]
        tempP = (1 + cnt2[bigamyStr]) / (cnt1[strList[i]] + len1 * len1)
        p = p * tempP
    return p
f = open("data.txt", "r", encoding="utf-8")
cnt1 = Counter()
cnt2 = Counter()
for line in f.readlines():
    words = line.split()
    temp1 = len(words)
    for i in range(temp1):
        cnt1[words[i]] += 1
        if i != temp1 - 1:
            cnt2[words[i] + words[i + 1]] += 1
f.close()
print(cnt1["中国"])
print(len(cnt1))
print(cnt2["在中国"])
print(len(cnt2))
print(cnt2['中国'])
# print(f"字典长度为:{dic.s}")
print(add1(cnt1,cnt2,"在的"))
print(add1(cnt1,cnt2,"的在"))

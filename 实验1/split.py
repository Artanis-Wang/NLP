def reData(inputFile, outputFile):
    """
    该函数用于处理最原始的语料，删去每句话开头的时间戳，以及词性标注，并生成一个新的txt文件
    :param inputFile: 最原始语料文件名
    :param outputFile: 目标文件名
    :return:
    """
    import re
    punc = r"""！？｡＂＃＄％＆＇《》（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.#$%&'()*+,-./:;<=>?@[\]^_`{
    |}~“”？，！【】（）、。：；’‘……￥· """

    f = open(inputFile, "r", encoding="gbk")
    fw = open(outputFile, "w+", encoding="utf-8")
    for line in f.readlines():
        wordList = line.strip().split()
        tempStr = "BOS "
        for word in wordList[1:]:
            words = word.split("/")  # 却掉/后面的词性标注
            word1 = words[0]
            tempStr = tempStr + word1 + " "  # 补上空格用以后续分割
        tempStr += " EOS"
        fw.write(re.sub(r"[%s]+" % punc, " ", tempStr))  # 根据正则表达式去除标点符号
        fw.write("\n")  # 补写换行符用以后续行遍历
    fw.close()
    f.close()


if __name__ == '__main__':
    reData("199801.txt", "data.txt")
    f = open("data.txt", "r", encoding="utf-8")
    data = f.readline()
    print(data)
    f.close()

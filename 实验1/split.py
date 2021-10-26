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
            words = word.split("/")
            word1 = words[0]
            tempStr = tempStr + word1 + " "
        tempStr += " EOS"
        fw.write(re.sub(r"[%s]+" % punc, " ", tempStr))
        fw.write("\n")
    fw.close()
    f.close()


if __name__ == '__main__':
    reData("199801.txt", "data.txt")
    f = open("data.txt", "r", encoding="utf-8")
    data = f.readline()
    print(data)
    f.close()
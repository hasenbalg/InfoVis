
import sys
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.text import Text
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import html.parser
from nltk.stem import WordNetLemmatizer
import json
from nltk.tokenize import sent_tokenize

import multiprocessing

def main():
    if not sys.argv[1]:
        return
    # read text
    text = open(sys.argv[1], "r").read()
    #remove tags
    text = re.sub('<.+?>', ' ', text)
    text = html.parser.HTMLParser().unescape(text)
    text_to_chop_in_sentences = text # for later use
    text = text.lower()

    # https://pythonprogramming.net/tokenizing-words-sentences-nltk-tutorial/
    # http://www.nltk.org/book/ch03.html
    tokens = word_tokenize(text)
    textList = Text(tokens)
    # textList.concordance('is')
    # print(tokens)
    # print()
    # print("simsilat to asian")
    # print(textList.similar("asian"))
    # print()
    # print("common context trunk, big")
    # print(textList.common_contexts(["trunk", "big"]))

    # remove puctuation
    textList = [w for w in textList if w.isalnum()]



    lemmatizer = WordNetLemmatizer()
    lemmata = []
    for word in textList:
        lemmata.append(lemmatizer.lemmatize(word))

    # get lemmata in order of freq
    # http://www.nltk.org/book/ch01.html
    fdist1 = FreqDist([w.lower() for w in lemmata if w not in set(stopwords.words('english'))])

    # make json
    # rs = json.dumps(dict(fdist1.most_common(50)))
    rs = make_json_from_tuple(fdist1.most_common(50), textList)
    print(rs)

    ################################################################################



    output = []
    most_common = fdist1.most_common(20)
    # http://stackoverflow.com/a/4119142/4062341
    chunkIt = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    chunks = chunkIt(most_common,len(most_common)%8)
    # http://stackoverflow.com/a/22391818/4062341
    params = [[c, most_common, text_to_chop_in_sentences] for c in chunks]

    # https://docs.python.org/3.4/library/multiprocessing.html
    pool = multiprocessing.Pool(processes = 8)
    res = pool.map(find_proximities, params)
    # print(res)
    output = []
    for r in res:
        output.extend(r)



    l = make_json_from_triple(merge_proximities(output))
    print (l)


    # occurence over text length
    output_list = []
    for word in fdist1.most_common(20):
        word = word[0]
        temp = (word, [])
        counter = 0;
        for word_in_text in textList:
            counter += 1
            if word == word_in_text:
                temp[1].append(counter)
        output_list.append(temp)
    output = ""
    for tuple in output_list:
        output += "{name: '" + tuple[0] + "', positions: " + str(tuple[1]) + " },"
    print('var occurences = [' + output.rstrip(',') + ']')


def find_proximities(param):
    chunk = param[0]
    most_common = param[1]
    text_to_chop_in_sentences = param[2]
    proximities = []

    for word1 in [w[0] for w in chunk]:
        for word2 in [w[0] for w in most_common]:
            if word1 is word2 or (word2, word1,0) in [(t[0],t[1],0) for t in proximities]:
                continue
            counter  = 0
            for sentence in sent_tokenize(text_to_chop_in_sentences):
                if(word1 in sentence and word2 in sentence):
                    counter += 1
            if counter > 0:
                proximities.append((word1, word2, counter))
    return proximities

def merge_proximities(data):
    output = []
    # order first and second word
    for tuple in data:
        new_t = (tuple[0], tuple[1])
        new_t = sorted(new_t)
        new_t = (new_t[0], new_t[1], tuple[2])
        output.append(new_t)
    return set(output) # remove doubles

def make_json_from_triple(list):
    output = ""
    for t in list:
        # https://mkaz.tech/code/python-string-format-cookbook/
        output += "{" + ("'w1': '{}',  'w2':'{}','sente': {}".format(t[0], t[1], t[2])) + "},"
    return "var links = [" + output.rstrip(',') + "];"

def make_json_from_tuple(list, textList):
    # make freqs
    max_occurence = 0;
    for t in list:
        if t[1] > max_occurence:
            max_occurence = t[1]

    max_tf = max_occurence/len(textList)

    output = ""
    for t in list:
        # https://mkaz.tech/code/python-string-format-cookbook/
        output += "{" + ("'word': '{}', 'idf': {}".format(t[0], (t[1]/len(textList))/max_tf)) + "},"
    return "var frequencies = [" + output.rstrip(',') + "];"


if __name__ == '__main__':
    main()

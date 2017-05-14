
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

import threading
import time


class myThread (threading.Thread):
   def __init__(self,chunk, most_common, text_to_chop_in_sentences):
      threading.Thread.__init__(self)
      self.chunk = chunk
      self.most_common = most_common
      self.text_to_chop_in_sentences = text_to_chop_in_sentences
   def run(self):
       #  print ("Starting " + self.name)
      pre_output = find_proximities(self.chunk, self.most_common ,self.text_to_chop_in_sentences)
      # Get lock to synchronize threads
      mutex.acquire()
      output.extend(pre_output)
      mutex.release()


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
    fdist1 = FreqDist([w.lower() for w in lemmata if w not in set(stopwords.words('english'))])

    # make json
    rs = json.dumps(dict(fdist1.most_common(500)))
    print(rs)

    ################################################################################


    thread_count = 8
    mutex = threading.Lock()
    threads = []
    output = []
    most_common = fdist1.most_common(500)
    # http://stackoverflow.com/a/4119142/4062341
    chunkIt = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    chunks = chunkIt(most_common,len(most_common)%thread_count)


    for i in range(0, thread_count):
        t = myThread(chunks[i], most_common ,text_to_chop_in_sentences)
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
       t.join()
    print ("Exiting Main Thread")
    print (output)



    l = make_json_from_triple(merge_proximities(output))
    print (l)


def find_proximities(chunk, most_common, text_to_chop_in_sentences):
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
        output += "{" + ("'w1': '{}',  'w2':'{}','sente': {}".format(t[0], t[1], t[2])) + "},"
    return "{" + output.rstrip(',') + "},"


if __name__ == '__main__':
    main()

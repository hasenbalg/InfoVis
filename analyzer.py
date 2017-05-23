# class Text(object):
#     def __init__(self):
#         self.paragraphs = []
#
#     def add_paragraph(self, paragraph):
#         self.paragraphs.append(paragraph)
#
# class Paragraph(object):
#     def __init__(self):
#         self.heading
#         self.sentences = []
#
#     def add_heading(self, heading):
#         self.heading = heading
#
#     def add_sentence(self, sentence):
#         self.sentences.append(sentence)
#
# class Sentence(object):
#     def __init__(self):
#         self.words = []
#
# class Word(object):
#     def __init__(self):
#         self.word
#         self.positions = []
#         self.idf

import sys
import re
import html.parser
from nltk.tokenize import word_tokenize
from nltk.text import Text
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize


paragraph_end_token = 'xxxendparagraphxxx'
heading_end_token = 'xxxendheadingxxx'


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



def main():
    if not sys.argv[1]:
        return
    # read text
    text = open(sys.argv[1], "r").read()

    # remove script
    # text = re.sub(r'<script.+?>(.+?)</script>', ' ', text)
    text = re.sub(r'<script[\s\S]+?</script>', ' ', text)

    # set *end_tokens
    text = re.sub(r'</p>',' ' +  paragraph_end_token + ' ', text)
    text = re.sub(r'</h[\d]>', ' ' +  heading_end_token + ' ', text)
    #remove tags
    text = re.sub(r'<.+?>', ' ', text)
    text = html.parser.HTMLParser().unescape(text)
    text_to_chop_in_sentences = text # for later use
    text = text.lower()
    # remove quote referneces
    text = re.sub(r'\[.+?\]', ' ', text)
    # remove html comments
    text = re.sub(r'<!--[^>]*-->', ' ', text)

    # print (text)

    # tokenize the text
    # https://pythonprogramming.net/tokenizing-words-sentences-nltk-tutorial/
    # http://www.nltk.org/book/ch03.html
    tokens = word_tokenize(text)
    textList = Text(tokens)


    # find full stops and paragraphs
    full_stops = []
    paragraphs = []
    for i in range(0, len(textList)):
        if textList[i] is '.':
            full_stops.append(i)

        if textList[i] in paragraph_end_token:
            paragraphs.append(i)

    print('var title = "' + str(sys.argv[1]) + '";')
    print('var full_stops = ' + str(full_stops) + ';')
    print('var paragraphs = ' + str(paragraphs) + ';')

    # remove puctuation and *end_tokes
    textList_with_punctuation = textList
    textList = [w for w in textList if w.isalnum() and w not in [paragraph_end_token ,heading_end_token]]

    # print('var text_length = ' + str(len(textList)) + ';')

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    lemmata = []
    for word in textList:
        lemmata.append(lemmatizer.lemmatize(word))

    # get lemmata in order of freq and get rid of crippled words(length < 2)
    # http://www.nltk.org/book/ch01.html
    fdist1 = FreqDist([w.lower() for w in lemmata if w not in set(stopwords.words('english')) and len(w) > 2])

    histogram = make_json_from_tuple(fdist1.most_common(50), textList)
    print(histogram)

    # force
    word_list = [w[0] for w in fdist1.most_common(10)]
    nodes = ''
    for word in word_list:
        nodes += "{'name': '" + word + "' },"

    links = ''
    sentences_list = sent_tokenize(text_to_chop_in_sentences)

    for i in range(len(word_list)):
        for j in range(len(word_list)):
            if word_list[i] is word_list[j]:
                continue
            counter = 0
            for sentence in sentences_list:
                if word_list[i] and word_list[j] in sentence:
                    counter += 1
            if counter > 0:
                links += "{'source':" + str(i) + ",'target':" + str(j) + ",'value':" + str(counter) + "},"

    print("var force_data = {'nodes': [" + nodes + "], 'links': [" + links + "]};")

    # dispersion plot
    word_list = [w[0] for w in fdist1.most_common(10)]
    word_list.extend([paragraph_end_token, '.'])
    dispositions = ''
    for word1 in word_list:
        counter = 0
        indecies = []
        for word2 in textList_with_punctuation:
            if word1 in word2:
                indecies.append(counter)
            counter += 1
        dispositions += "{name : '" + word1 + "', positions: " + str(indecies) + "},"

    # dispositions += "{name : 'huhu', positions: [1,3,5,7,9, 10]},{name : 'haha', positions: [2,4,6,8]},{name : 'hihi', positions: [3,4,7,15]},{name : 'hoho', positions: [3,4,7,15, 17, 12]}"
    print("var dispositions = [" + dispositions + "];")
    print("var text_length = " + str(len(textList)) + ";")

    #mini map
    output = []
    for word in textList:
        if word in [paragraph_end_token, heading_end_token]:
            output.append('\n')
        else:
            output.append(word)
    print("var mini_map = " + str(output) + ";")

if __name__ == '__main__':
    main()

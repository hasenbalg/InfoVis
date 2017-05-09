import re
import sys
import string
import html.parser
import nltk

stopwords = []

def get_rid_of_tags(raw_html):
    # http://stackoverflow.com/a/12982689
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_rid_of_puctuation(text):
    cleanr = re.compile('[^\w\s&;]')
    cleantext = re.sub(cleanr, '', text)
    return cleantext

def get_rid_of_linebreaks(text):
    cleanr = re.compile('[\n\t]')
    cleantext = re.sub(cleanr, ' ', text)
    return cleantext

def unescape_html(text):
    return html.parser.HTMLParser().unescape(text)

def get_most_important_words(text):
    text = text.lower()
    important_words = []
    tags = ['h\d','b']
    for tag in tags:
        cleanr = re.compile('<' + tag + '>(.+?)<\/' + tag + '>')
        for sentence in re.findall(cleanr, text):
            sentence = get_rid_of_tags(sentence)
            sentence = get_rid_of_puctuation(sentence)
            sentence = get_rid_of_linebreaks(sentence)
            for word in sentence.split():
                important_words.append(word)
    lemmata = []
    for w in important_words:
        if w.lower() not in stopwords:
            lemmata.append(w)
    # return nltk.FreqDist(lemmata).most_common(100)
    return lemmata

def get_most_common_words(text):
    text = text.lower()
    lemmata = []
    for w in text.split(' '):
        w = get_rid_of_puctuation(w)
        w = get_rid_of_linebreaks(w)
        if w.lower() not in stopwords:
            lemmata.append(w)
    # return nltk.FreqDist(lemmata).most_common(100)
    return lemmata


def main():
    global stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(["fig", "also", "becomes", ";"])
    if not sys.argv[1]:
        return
    # read text
    html = open(sys.argv[1], "r").read()
    html = unescape_html(html)
    # get bold words
    important_words = get_most_important_words(html)
    print()
    print()
    print("important_words")
    print(important_words)

    text = get_rid_of_tags(html)
    text = get_rid_of_puctuation(text)

    most_common_words = get_most_common_words(text)
    print()
    print()
    print("most_common_words")
    print(most_common_words)

    # merge most_common_words with important_words
    lemmata = most_common_words + important_words
    lemmata = list(filter(None, lemmata)) # remove emptys
    print()
    print()
    print("lemmata")
    print(lemmata)


    # lemmatizing
    lemmatized = []
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for lemma in lemmata:
        lemmatized.append(lemmatizer.lemmatize(lemma))


    lemmatized = nltk.FreqDist(lemmatized).most_common(1000)
    print()
    print()
    print("lemmatized")
    print(lemmatized)

    # stemming
    stemmed = []
    ps = nltk.stem.PorterStemmer()
    for lemma in lemmata:
        stemmed.append(ps.stem(lemma))

    stemmed = nltk.FreqDist(stemmed).most_common(1000)
    print()
    print()
    print("stemmed")
    print(stemmed)


if __name__ == '__main__':
    main()

import re
import sys
class Lemma(object):

    def __init__(self,name, position):
        self.name = name
        self.positions = [position]
    def add_position(self, position):
        self.positions.append( position)

    def and_where(self):
        output = self.name + " "
        for pos in self.positions:
            output += " " + str(pos)
        #output += "\n"
        return output;
    @staticmethod
    def stemming(word):
        word = re.sub("s$","",word)
        word = re.sub("ing$","",word)
        word = re.sub("ed$","",word)
        word = re.sub("ly$","",word)
        # word = re.sub("ish$","",word)
        return word

    def idf(self, lemmata, text_length):
        most_common_lemma_pos_len = 0;
        for lemma in lemmata:
            if len(lemma.positions) > most_common_lemma_pos_len :
                most_common_lemma_pos_len =len(lemma.positions)
        df = len(self.positions)/float(text_length)
        most_df = most_common_lemma_pos_len/float(text_length)
        return df/most_df



#########################################################
def get_avg_word_distance(word1, word2, text):
    if word1 is word2:
        return

    distances = []
    counter = 0;
    counting = False
    # foreward
    for w in text:
        if w in word1:
            counting = True
        if w in word2:
            counting = False
            if counter > 0:
                distances.append(counter)
                counter = 0
        if counting:
            counter +=1
    # backward
    for w in text:
        if w in word2:
            counting = True
        if w in word1:
            counting = False
            if counter > 0:
                distances.append(counter)
                counter = 0
        if counting:
            counter +=1
    # print distances
    return sum(distances) / float(len(distances))



def main():
    text = [];
    lemmata = []
    static_stop_words = ["an","are","was","at","with","from", "can", "its", "they","were", "other", "more","it","by","is", "after","for","that","on","up","in","to","and","a","of","the","or","he","she","nor","ether","their","that","this","you","then","than","if","when","as", "has", "be", "have", "been", "which", "his", "her"]

    for line in open(sys.argv[1], "r"):
        line = line.strip()
        if len(line) > 0:
            for word in line.split():
                    word  = filter(str.isalnum, word).lower()
                    text.append(word)

    print str(len(text)) + " Woerter gefunden"

    #collect double words
    i = 0;
    for word in text:
        allready_exists = False
        if word not in static_stop_words and len(word) > 1:
            word = Lemma.stemming(word)
            for w in lemmata:
                if w.name == word:
                    w.add_position(i)
                    allready_exists = True
            if not allready_exists:
                lemmata.append(Lemma(word, i))
        i+=1

    print str(len(lemmata)) + " unterschiedliche Woerter gefunden"

    #sort lemmata
    lemmata = sorted(lemmata, key=lambda word: len(word.positions))
    #find stop words
    # stop_words = []
    # for word in lemmata:
    #     if word.idf(lemmata, len(text)) >= .076:
    #         stop_words.append(word)
    # print str(len(stop_words)) + " stop words found"

    #remove stop words
    # for word in lemmata:
    #     for stop_word in stop_words:
    #         if word.name == stop_word.name:
    #             lemmata.remove(word)
    # print len(lemmata)

    #sort stop words
    # stop_words = sorted(stop_words, key=lambda word: len(word.positions))
    # for word in stop_words:
    #     print word.name

    for lemma in lemmata[-9:]: # last 10 of list
        print "{"
        print "\"name\": " + "\"" + lemma.name + "\"" + ","
        print "\"idf\": " + str(lemma.idf(lemmata, len(text))) + ","
        print "\"avg_distance\": " + str(get_avg_word_distance(lemmata[len(lemmata)-1].name, lemma.name, text))
        print "},"


    # print lemmata[len(lemmata)-1].name, lemmata[len(lemmata)-2].name
    # print(get_avg_word_distance(lemmata[len(lemmata)-1].name, lemmata[len(lemmata)-2].name, text))
    # print lemmata[len(lemmata)-1].name, lemmata[len(lemmata)-3].name
    # print(get_avg_word_distance(lemmata[len(lemmata)-1].name, lemmata[len(lemmata)-3].name, text))
    # print lemmata[len(lemmata)-1].name, lemmata[len(lemmata)-4].name
    # print(get_avg_word_distance(lemmata[len(lemmata)-1].name, lemmata[len(lemmata)-4].name, text))


if __name__ == '__main__':
    main()

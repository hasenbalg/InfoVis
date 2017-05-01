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

    for lemma in lemmata:
        print lemma.name


if __name__ == '__main__':
    main()


class Word(Object):
    def __init__(self, name):
        self.name = name
    def set_bold(self):
        self.is_bold = True

class Sentence(Object):
    def __init__(self, words):
        self.words = words

class Paragraph(Object):
    def __init__(self, heading, sentences):
        self.heading = heading
        self.sentences = sentences

def main():
    
if __name__ == '__main__':
    main()

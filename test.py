#!/usr/bin/env python3
from invert import Invert
import json

class Test:
    stopwordToggle = False
    posting_list = {}

    def __init__(self):
        invert = Invert()
        self.stopwordToggle = False
        self.posting_list = json.load(open('posting-list.json', 'r'))
        self.search_user_input()

    def search_user_input(self):
        data = input('Enter a search term or stopword to toggle stopwords\n')
        while data is not None:
            word = data.lower()
            print(word)
            if len(word.split(' ')) > 1:
                print('please enter one word')
            elif 'stopword' in word:
                use_stop_words = input('use stop words? (y/n)\n')
                while use_stop_words is not None:
                    if use_stop_words.lower() == 'y':
                        self.stopwordToggle = True
                        print('Stopwords are being used in the search')
                        break
                    elif use_stop_words.lower() == 'n':
                        self.stopwordToggle = False
                        print('Stopwords are not being used in the search')
                        break
                    use_stop_words = input('please enter y or n\n')
            else:
                self.search_term(word, self.stopwordToggle)
            data = input('')

    def search_term(self, word, stopwordToggle):
        print(self.posting_list[word])


if __name__ == '__main__':
    t = Test()

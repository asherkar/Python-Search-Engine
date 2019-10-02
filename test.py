#!/usr/bin/env python3
from file import File

import fileinput

f = File()
stopwordToggle = False

for word in fileinput.input():
    word = word.lower()
    print(word)
    if word.split(' ').lenth > 1:
        print('please enter one word')
    else if 'stopword' in line:
        print('use stop words? (y/n)')
    else:
        search_word(word, stopwordToggle)


def search_word(word, stopwordToggle):


#!/usr/bin/env python3
import re
import json
from porter import PorterStemmer
import time
import random

then = time.time()       ##start timer

documents = {}
terms = {}
termsDictionary = {}


class File:

    f = None
    p = None

    def __init__(self):
        f = open('cacm/cacm.all', 'r')
        p = PorterStemmer()
        self.parse_documents(f, p)

    def parse_documents(self, f, p):
        line = f.readline()
        while line:
            line = line
            nextLine = None

            if '.I ' in line:
                docId = re.sub('.I ', '', line).rstrip()
                documents[docId] = {}
                documents[docId]['id'] = docId
                nextLine = f.readline()

                while nextLine and not ('.I ' in nextLine):
                    if '.W' in nextLine:
                        nextLine = f.readline()
                        abstract = ''
                        while nextLine and not re.match(r'[.][A-Z]\s', nextLine):
                            abstract += ' ' + nextLine.rstrip()
                            nextLine = f.readline()
                        documents[docId]['abstract'] = abstract

                    if '.T ' in nextLine:
                        documents[docId]['title'] = f.readline().rstrip()

                    if '.B' in nextLine:
                        documents[docId]['publication'] = f.readline().rstrip()
                    if '.A' in nextLine:
                        documents[docId]['author'] = f.readline().rstrip()

                    nextLine = f.readline()

            line = f.readline() if nextLine is None else nextLine

        for doc_id, document in documents.items():
            if 'abstract' in document:
                for index, word in enumerate(document['abstract'].split(' ')):
                    for a in [',', '.', '{', '}', '(', ')', ';', ':', '"', '\'']:
                        word = word.replace(a, '')
                    word = p.stem(word, 0, len(word) - 1)
                    word = word.rstrip().lower()

                    if len(word) > 0:
                        if word not in terms.keys():
                            terms[word] = {}

                        if doc_id not in terms[word].keys():
                            terms[word][doc_id] = {
                                'frequency': 0,
                                'position': []
                            }

                        terms[word][doc_id]['frequency'] += 1
                        terms[word][doc_id]['position'].append(index)

        for term, value in terms.items():
            termsDictionary[term] = len(value)

        f.close()

        f = open('dictionary.json', 'w+')
        f.write(json.dumps(termsDictionary))
        f.close()

        f = open('posting-list.json', 'w+')
        f.write(json.dumps(terms))
        f.close()


    now = time.time() ##stop timer

    print("total time: ", round(now-then, 3), " seconds")
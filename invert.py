#!/usr/bin/env python3
import re
import json
from porter import PorterStemmer


class Invert:

    f = None
    p = None
    then = None
    documents = {}
    terms = {}
    termsDictionary = {}

    def __init__(self, stopword_toggle = False, stemming_toggle = False):
        self.documents = self.parse_documents()
        self.create_posting_list(stopword_toggle, stemming_toggle)

    def parse_documents(self):
        f = open('cacm/cacm.all', 'r')
        documents = self.documents
        line = f.readline()
        while line:
            next_line = None

            if '.I ' in line:
                doc_id = re.sub('.I ', '', line).rstrip()
                documents[doc_id] = {
                    'id': doc_id,
                    'title': '',
                    'abstract': '',
                    'publication': '',
                    'author': ''
                }
                next_line = f.readline()

                while next_line and not ('.I ' in next_line):
                    if '.W' in next_line:
                        next_line = f.readline()
                        abstract = ''
                        while next_line and not re.match(r'[.][A-Z]\s', next_line):
                            abstract += ' ' + next_line.rstrip()
                            next_line = f.readline()
                        documents[doc_id]['abstract'] = abstract

                    if '.T' in next_line:
                        documents[doc_id]['title'] = f.readline().rstrip()

                    if '.B' in next_line:
                        documents[doc_id]['publication'] = f.readline().rstrip()
                    if '.A' in next_line:
                        documents[doc_id]['author'] = f.readline().rstrip()

                    next_line = f.readline()

            line = f.readline() if next_line is None else next_line

        f.close()
        return documents

    def create_posting_list(self, stopword_toggle, stemming_toggle):
        self.terms = {}
        self.termsDictionary = {}
        documents = self.documents
        stopwords = []
        if stopword_toggle:
            stopwords = self.fetch_stopwords()
        for doc_id, document in documents.items():
            if 'abstract' in document:
                for index, word in enumerate(document['abstract'].split(' ')):
                    word = word.rstrip().lower()

                    for a in [',', '.', '{', '}', '(', ')', ';', ':', '"', '\'']:
                        if a in word:
                            if word.index(a) == 0 or word.index(a) == len(word) - 1:
                                word = word.replace(a, '')
                    if stemming_toggle:
                        p = PorterStemmer()
                        word = p.stem(word, 0, len(word) - 1)

                    if word in stopwords:
                        continue

                    if len(word) > 0:
                        if word not in self.terms.keys():
                            self.terms[word] = {}

                        if doc_id not in self.terms[word].keys():
                            self.terms[word][doc_id] = {
                                'frequency': 0,
                                'position': [],
                            }

                        self.terms[word][doc_id]['frequency'] += 1
                        self.terms[word][doc_id]['position'].append(index)

        for term, value in self.terms.items():
            self.termsDictionary[term] = len(value)

        f = open('dictionary.json', 'w')
        f.write(json.dumps(self.termsDictionary, indent=4, sort_keys=True))
        f.close()

        f = open('posting-list.json', 'w')
        f.write(json.dumps(self.terms, indent=4, sort_keys=True))
        f.close()

    def fetch_stopwords(self):
        file = open('cacm/common_words')
        stopwords = []
        for word in file:
            stopwords.append(word.rstrip())
        file.close()
        return stopwords

#!/usr/bin/env python3
from invert import Invert
from porter import PorterStemmer
import json
import time


class Test:
    stopword_toggle = False
    posting_list = {}
    term_dictionary = {}
    invert = Invert()

    def __init__(self):
        self.stopword_toggle = False
        self.stemming_toggle = False
        self.load_files()
        self.search_user_input()

    def search_user_input(self):
        data = input('Enter a search term or stopword to toggle stopwords\n')
        while data is not None:
            word = data.lower()
            if len(word.split(' ')) > 1:
                print('please enter one word')
            elif 'HELP' in data:
                print('Enter stopword to toggle the use of stopwords')
                print('Enter stemming to toggle the use of stemming')
                print('Enter ZZEND to exit')
            elif 'stopword' in word:
                use_stop_words = input('use stop words? (y/n)\n')
                while use_stop_words is not None:
                    if use_stop_words.lower() == 'y':
                        print(len(self.posting_list))
                        self.stopword_toggle = True
                        self.invert.create_posting_list(self.stopword_toggle, self.stemming_toggle)
                        self.load_files()
                        print('Stopwords are being used in the search')
                        print(len(self.posting_list))
                        break
                    elif use_stop_words.lower() == 'n':
                        self.stopword_toggle = False
                        self.invert.create_posting_list(self.stopword_toggle, self.stemming_toggle)
                        self.load_files()
                        print('Stopwords are not being used in the search')
                        break
                    use_stop_words = input('please enter y or n\n')

            elif 'stemming' in word:
                use_stemming = input('stem the words? (y/n)\n')
                while use_stemming is not None:
                    if use_stemming.lower() == 'y':
                        print(len(self.posting_list))
                        self.stemming_toggle = True
                        self.invert.create_posting_list(self.stopword_toggle, self.stemming_toggle)
                        self.load_files()
                        print('the words are now being stemmed in search')
                        print(len(self.posting_list))
                        break
                    elif use_stemming.lower() == 'n':
                        self.stemming_toggle = False
                        self.invert.create_posting_list(self.stopword_toggle, self.stemming_toggle)
                        self.load_files()
                        print('the words are not being stemmed in search')
                        break
                    use_stemming = input('please enter y or n\n')
            elif data == 'ZZEND':
                print('exiting program')
                exit()
            else:
                self.search_term(word)
            data = input('Enter a search term or HELP for more options\n')

    def load_files(self):
        f = open('posting-list.json', 'r')
        self.posting_list = json.load(f)
        f.close()
        f = open('dictionary.json', 'r')
        self.term_dictionary = json.load(f)
        f.close()
        print(len(self.posting_list))

    def search_term(self, word):
        start_time = time.time()  ##start timer
        if self.stemming_toggle:
            p = PorterStemmer()
            word = p.stem(word, 0, len(word) - 1)

        if word in self.term_dictionary:
            found_items = self.posting_list[word]
            found_documents = []
            document_ids = found_items.keys()
            for doc_id in document_ids:
                position = found_items[doc_id]['position']
                abstract = self.invert.documents[doc_id]['abstract'].split(' ')
                first_pos = position[0]
                start_pos = 0
                end_pos = len(abstract) -1
                summary = ''
                if len(abstract) > 10:
                    start_pos = first_pos - 5
                    if start_pos < 0:
                        start_pos = 0

                    end_pos = start_pos + 10

                    if end_pos > len(abstract) -1:
                        end_pos = len(abstract) -1
                        start_pos = end_pos - 10

                for word in abstract[start_pos:end_pos]:
                    summary += word + ' '

                document = {
                    'doc_id': doc_id,
                    'title': self.invert.documents[doc_id]['title'],
                    'term frequency': found_items[doc_id]['frequency'],
                    'positions': position,
                    'summary': summary
                }
                found_documents.append(document)

            print(json.dumps(found_documents, indent=4, sort_keys=True))
            end_time = time.time()  ##start timer
            print("Found " + str(self.term_dictionary[word]) + "  items in ", round(end_time - start_time, 3), " seconds")
        else:
            print('No results found for the term ' + word)



if __name__ == '__main__':
    t = Test()

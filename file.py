#!/usr/bin/env python
import re

documents = {}
f = open('cacm/test.txt', 'r')

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
            if '.T ' in nextLine:
                documents[docId]['title'] = f.readline().rstrip()

            if '.W' in nextLine:
                nextLine = f.readline()
                abstract = ''
                while nextLine and not re.match(r'[.][A-Z]\s', nextLine):
                    abstract += ' ' + nextLine.rstrip()
                    nextLine = f.readline()
                documents[docId]['abstract'] = abstract

            if '.B' in nextLine:
                documents[docId]['publication'] = f.readline().rstrip()
            if '.A' in nextLine:
                documents[docId]['author'] = f.readline().rstrip()

            nextLine = f.readline()


    line = f.readline() if nextLine is None else nextLine
        
    
print(documents)


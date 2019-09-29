#!/usr/bin/env python
import re

documents = {}
f = open('cacm/test.txt', 'r')

line = f.readline().rstrip()
while line:
    nextLine = None

    if '.I ' in line:
        docId = re.sub('.I ', '', line)
        documents[docId] = {}
        documents[docId]['id'] = docId
        nextLine = f.readline().rstrip()
        print(nextLine)

        while nextLine and not ('.I ' in nextLine):
            print(nextLine)
            if '.T' in nextLine:
                documents[docId]['title'] = f.readline()
            if '.W' in nextLine:
                nextLine = f.readline().rstrip()
                abstract = ''
                while nextLine and not re.match(r'^[.][A-Z]\s', nextLine):
                    print(nextLine)
                    abstract += ' ' + nextLine
                    nextLine = f.readline().rstrip()
                documents[docId]['abstract'] = abstract
            nextLine = f.readline().rstrip()
            print(nextLine)

    line = f.readline() if nextLine is None else nextLine
        
    
print(documents)


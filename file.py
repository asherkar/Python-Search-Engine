#!/usr/bin/env python
import re

documents = {}
f = open('cacm/test.txt', 'r')

for line in f:
    line = line.rstrip()
    print(line)
    if '.I ' in line:
        id = re.sub('.I ', '', line)
        print(id)
        documents[id] = {}
        documents[id]['id'] = id
        nextLine = f.next()

        while(not ('.I ' in nextLine)):
            if '.T' in nextLine:
                documents[id]['title'] = f.next()
            if '.W' in nextLine:
                nextLine = f.next()
                abstract = ''
                while(re.match(r'^[.][A-Z]\s', nextLine)):                    
                    abstract+= nextLine
                    nextLine = f.next()
                documents[id]['abstract'] = abstract
            nextLine = f.next()
        
    
print(documents)


#!/usr/bin/env python
import re

documents = {}
f = open('cacm/cacm.all', 'r')

for line in f:
    if '.I ' in line:
        id = re.sub('.I ', '', line)
        documents[id] = {'id' : id}
        print(id)
    if '.T' in line:
        print(f.next())


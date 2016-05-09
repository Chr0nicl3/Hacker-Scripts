#!/usr/bin/python

import re

words = open('/root/Desktop/hts/scramble.txt' , 'r')
scrambles = list()
final = list()
ans = list()

#scramble.txt to list
for word in words:
    scrambles.append(word)

for test in scrambles:
    if test == "\n":
        scrambles.remove(test)

for test in scrambles:
    l = len(test)-1
    final.append(test[:l])

#unscramble
for word in final:
    i = len(word)
    wordlist = open('/root/Desktop/hts/wordlist.txt' , 'r')
    pattern = "[%s]{%d}"%(word,i)
    compiled = re.compile(pattern)
    for line in wordlist:
        match = re.findall(compiled , line)
        if match == None:
            continue
        elif match!=None and len(match)!=0 and sum(bytearray(match[0]))==sum(bytearray(word)):
            ans.append(match[0])

for word in ans:
    print "%s,"%(word),

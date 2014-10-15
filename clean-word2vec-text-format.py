#!/usr/bin/python

import codecs
import os
import shutil

SOURCE = 'glove.840B.300d.txt'
TARGET = 'glove.840B.300d--modified.txt'
TMP = 'tmp.file'

LENGTH_BY_PREFIX = [
  (0xC0, 2), # first byte mask, total codepoint length
  (0xE0, 3), 
  (0xF0, 4),
  (0xF8, 5),
  (0xFC, 6),
]

def codepoint_length(first_byte):
    if first_byte < 128:
        return 1 # ASCII
    for mask, length in LENGTH_BY_PREFIX:
        if first_byte & mask == mask:
            return length
        else:
            return 0

def read_utf8_char_and_decode(source):
    c = source.read(1)
    if c:
        char_len = codepoint_length(ord(c))
    else:
        return u''
    if char_len:
        c += source.read(char_len-1)
        try:
            c=c.decode('utf8')
        except:
            return u''
    else:
        return u''
    return c

source = open(SOURCE,mode='r')
tmp = codecs.open(TMP,mode='w',encoding='utf8')
line = source.readline()
vsize, nbdim = line.split()
vsize = int(vsize)
print vsize
count = 0
bad = 0
i = 0
wrong_chars = [u'',u'\u00A0',u'\u2026',u'\u000A', u'\u000B', u'\u000C', u'\u000D', u'\u0085', u'\u2028', u'\u2029']
print "Started ..."
while i<vsize:
    if i % 100000 == 0:
        print i
    i+=1
    s = u''
    c = u''
    while c != u' ':
        c = read_utf8_char_and_decode(source)
        if c in wrong_chars:
            if c:
	        print 'Error %s' % repr(c)
            bad+=1
            source.readline()
            break
        else:
            s += c
    if c in wrong_chars:
        continue
    s2 = source.readline()
    try:
        s2 = s2.decode('utf8')
    except:
        print "Error: %s" % s2
        bad += 1
        continue
    count += 1
    tmp.write(s+s2)

print "%d bad words" % bad
print "%d total word count" % count
print "Now copying to the target file..."

source.close()
tmp.close()

with codecs.open(TMP,mode='r',encoding='utf8') as tmp:
    with codecs.open(TARGET,mode='w',encoding='utf8') as target:
        target.write("%d 300\n" % (count))
        shutil.copyfileobj(tmp, target)

tmp.close()
target.close()
os.remove(TMP)

print("Done.")

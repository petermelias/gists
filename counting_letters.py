# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2013 Peter M. Elias

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE


'''
Concerning the problem of counting
specific characters in a string.

Here I present 2 pythonic approaches
and 2 algorithmic approaches
'''


x = 'babbceeeccdddzzzdeffgxxxxgggg'

# Method 1, using a dict / loop.

print '\nMethod 1: Counting in a dict\n'

d = {}
for c in x:
    try:
        count = d[c]
        d[c] += 1
    except KeyError:
        d[c] = 1
print d

# Method 2, using dict / count() / loop
# also a (sexy | confusing) one liner depending
# on how you feel about that sort of thing

print '\nMethod 2: Counting using str.count() and a dict\n'

d = {}
[d.update({c: x.count(c)}) for c in x if c not in d]
print d


# Method 3, using replacement as a form of reduction

print '\nMethod 3: Character reduction difference\n'

s = x
slen = len(s)
while slen > 0:
    c = s[0]
    s = s.replace(c, '')
    newlen = len(s)
    print 'There are %s occurences of %s' % (slen - newlen, c)
    slen = newlen

# Method 4, using a sorted approach

print '\nMethod 4: Sorted count\n'

sortedx = sorted(x)
last = None
count = 0
for c in sortedx:
    if not last:
        last = c
    if c != last:
        print 'There are %s occurences of %s' % (count, last)
        count = 0
        last = c
    count += 1

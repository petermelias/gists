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


# DictInterface implmentation left up to user. Suffice to say its easier if
# the objects can be easily representable in dict form

def graph(o):
    traversed = []
    graphed = {}

    def _traverse(o, prev_idx=None):
        traversed.append(o) if o not in traversed else None
        obj_idx = traversed.index(o)

        if prev_idx is not None:
            graphed[prev_idx].append(obj_idx)
        if obj_idx not in graphed.keys():
            graphed[obj_idx] = []
        else:
            return
        links = [getattr(o, k) for k, v in o.to_dict.iteritems() if isinstance(v, DictInterface)]
        [_traverse(l, obj_idx) for l in links]

    _traverse(o)
    return (graphed, traversed)

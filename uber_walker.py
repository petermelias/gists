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

from pprint import pprint

from inspect import getmembers, ismethod


node = 0


def next_node():
    global node
    current = node
    node += 1
    return current


def to_dict(o):
    m = getmembers(o, lambda x: not ismethod(x))
    return dict([i for i in m if not i[0].startswith('_')])


class Graphable(object):
    pass


class Parent(Graphable):

    def __init__(self):
        self.node_number = next_node()
        self.children = [Child(self), Child(self)]
        self.friends = []

    def add_friend(self, parent):
        self.friends.append(parent)


class Child(Graphable):

    def __init__(self, parent):
        self.node_number = next_node()
        self.parent = parent

    @property
    def siblings(self):
        return [c for c in self.parent.children if c is not self]

    @property
    def friends(self):
        return [c for c in [p.children for p in self.parent.friends]]


def _step():
    raw_input('S >')


def walk(value, graph_max=None, _graph_path=[], _graph_current=0):

    def _recur(v):
        return walk(v, graph_max, _graph_path, _graph_current)

    if isinstance(value, Graphable):
        if graph_max and _graph_current >= graph_max:
            return 'REC_MAX'

        if _graph_path:
            if len(_graph_path) >= 2 and value is _graph_path[-2]:
                return 'REC_MAX'
            elif value in _graph_path:
                return walk(to_dict(value), graph_max=1, _graph_path=[])

        _graph_path.append(value)
        _graph_current = _graph_current + 1

        value = to_dict(value)

    if type(value) is dict:
        d = {}
        for k, v in value.iteritems():
            r = _recur(v)
            if r == 'REC_MAX':
                continue
            d[k] = r
        return d
    if hasattr(value, '__iter__'):
        l = []
        for v in value:
            r = _recur(v)
            if r == 'REC_MAX':
                continue
            l.append(r)
        return l

    return value


p = Parent()
p.add_friend(Parent())
p.add_friend(Parent())

test = {
    'a_list': ['a', 'b', 'c', object],
    'b_list': {'oh': 'no', 'spaghetti': object},
    'value': 'simple',
    'people': p
}

pprint(walk(test))

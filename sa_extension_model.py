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

# This is for the scenario where you have 2 logical models
# whose association has metadata BUT you want the association
# sorted uniquely by the other object. This is a 1-way example.
# Making this bi-directional is trivial.


from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer
)

BaseClass = declarative_base()


class Parent(BaseClass):
    __tablename__ = 'parents'

    children = relationship('ChildAssociation',
                            passive_deletes=True,
                            collection_class=attribute_mapped_collection('child'))

    def add_child(self, child):
        random_data = {
            'i': 'am metadata'
        }

        try:
            assoc = self.children[child]
            assoc.meta = random_data
        except KeyError:
            self.children[child] = ChildAssociation(child, self, **random_data)

    def remove_child(self, child):
        try:
            del self.children[child]
        except KeyError:
            pass


class ChildAssociation(BaseClass):
    __tablename__ = 'child_parent_associations'

    child_id = Column(
        Integer, ForeignKey('children.id', ondelete='CASCADE'))
    child = relationship('Child', uselist=False)

    parent_id = Column(
        Integer, ForeignKey('parents.id', ondelete='CASCADE'))
    parent = relationship('Parent', uselist=False)

    def __init__(self, child, parent, **kw):
        self.child = child
        self.parent = parent
        self.meta = kw


class Child(BaseClass):
    __tablename__ = 'children'

# Usage:
p = Parent()
c = Child()
c2 = Child()

p.add_child(c)
p.add_child(c2)

print p.children

p.remove_child(c)

print p.children

print p.children[c2].meta  # the whole point of this

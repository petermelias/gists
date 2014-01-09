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

import csv
import datetime
import hashlib


def reorder(input_file, current_order=None, new_order=None, scrub=True, pk_index=0):
    output_filename = input_file.replace('.csv', '') + '_reordered.csv'
    with open(output_filename, 'w+') as fw:
        writer = csv.writer(fw)
        with open(input_file, 'rb') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    if scrub and not row[pk_index] or row[pk_index] == 'NULL':
                        continue
                    new_row = [0] * len(current_order)
                    for x in range(0, len(current_order)):
                        value = row[x]
                        value_name = current_order[row.index(value)]
                        new_row[new_order.index(value_name)] = value
                    writer.writerow(new_row)
            except csv.Error as e:
                print 'BLAHHHHHHHHHH: ' + e


def melt(input_files, dedupe=True, pk_index=0):
    output_filename = 'melt_%s.csv' % datetime.datetime.now()
    with open(output_filename, 'w+') as fw:
        writer = csv.writer(fw)
        master_by_pk = {}
        for input_file in input_files:
            with open(input_file, 'rb') as f:
                reader = csv.reader(f)
                try:
                    for row in reader:
                        if dedupe and row[pk_index].lower() in master_by_pk:
                            continue
                        master_by_pk[row[pk_index].lower()] = row
                except csv.Error as e:
                    print 'AAARGGGG: ' + e
        writer.writerows(master_by_pk.values())


def diff(block, chisel, pk_index=0):
    output_filename = '%s_diffed.csv' % block.replace('.csv', '')
    with open(output_filename, 'w+') as fw:
        writer = csv.writer(fw)
        chisels = []
        with open(chisel, 'rb') as fc:
            chisel_reader = csv.reader(fc)
            for row in chisel_reader:
                chisels.append(row[pk_index].lower())

        with open(block, 'rb') as fb:
            block_reader = csv.reader(fb)
            for row in block_reader:
                if row[pk_index].lower() not in chisels:
                    writer.writerow(row)


def append_field_hash(input_file, field_index=0, hash_field_index=1, hash_function=lambda x: hashlib.sha1(x).hexdigest()):
    output_filename = input_file.replace('.csv', '') + '_hashed.csv'
    with open(output_filename, 'w+') as fw:
        writer = csv.writer(fw)
        with open(input_file, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                value = row[field_index]
                if value:
                    hashed_value = hash_function(value)
                    new_row = row
                    new_row.insert(hash_field_index, hashed_value)
                    writer.writerow(new_row)

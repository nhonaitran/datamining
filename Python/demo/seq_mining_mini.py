# -*- coding: utf-8 -*-
"""
Created on Mon Dec 01 17:59:30 2014
MCT's python sequence mining solution. First try: use code from a random 
person on the internet.

Couldn't get it to extract correctly (probably designed for Linux), so I'll just copy/paste the relevent functions in...

Usage:
>>> from pymining import seqmining
    >>> seqs = ( 'caabc', 'abcb', 'cabc', 'abbca')
    >>> freq_seqs = seqmining.freq_seq_enum(seqs, 2)
    >>> sorted(freq_seqs)
    [(('a',), 4), (('a', 'a'), 2), (('a', 'b'), 4), (('a', 'b', 'b'), 2), (('a', 'b', 'c'), 4), 
     (('a', 'c'), 4), (('b',), 4), (('b', 'b'), 2), (('b', 'c'), 4), (('c',), 4), (('c', 'a'), 3), 
     (('c', 'a', 'b'), 2), (('c', 'a', 'b', 'c'), 2), (('c', 'a', 'c'), 2), (('c', 'b'), 3), 
     (('c', 'b', 'c'), 2), (('c', 'c'), 2)]


@author: mtho199
Code from Bart Dagenais
https://github.com/bartdag/pymining

"""
from collections import defaultdict
import os

def return_letter_code(item):
    if item == '1':
        return 'a'
    elif item == '2':
        return 'b'
    elif item == '3':
        return 'c'
    elif item == '4':
        return 'd'
    elif item == '5':
        return 'e'
    elif item == '6':
        return 'f'
    elif item == '7':
        return 'g'
    elif item == '8':
        return 'h'
    elif item == '9':
        return 'i'
    elif item == '10':
        return 'j'
    elif item == '11':
        return 'k'
    elif item == '12':
        return 'l'
    elif item == '13':
        return 'm'
    elif item == '14':
        return 'n'
    elif item == '15':
        return 'o'
    elif item == '16':
        return 'p'
    elif item == '17':
        return 'q'


def read_seq_file(filename):
    f = open(filename,"r")
    data_list = [] # Store data in list. Convert to tuple later
    for line in f:
        record = '' # initialize record
        if line[0] == ' ' or line[0] == '' or line[0] == '%' or line[0] == '\n':
            continue
        
        split_line = line.split()
        for index in range(0,len(split_line)):
            letter = return_letter_code(split_line[index])
#            split_line[index] = letter
            record = record + letter
        data_list.append(record)
    f.close()
    return tuple(data_list)


def freq_seq_enum(sequences, min_support,data_len):
    '''Enumerates all frequent sequences.

       :param sequences: A sequence of sequences.
       :param min_support: The minimal support of a set to be included.
       :rtype: A set of (frequent_sequence, support).
    '''
    freq_seqs = set()
    _freq_seq(sequences, tuple(), 0, min_support,data_len, freq_seqs)
    return freq_seqs


def _freq_seq(sdb, prefix, prefix_support, min_support,data_len, freq_seqs):
    if prefix:
        freq_seqs.add((prefix, prefix_support))
    locally_frequents = _local_freq_items(sdb, prefix, min_support,data_len)
    if not locally_frequents:
        return
    for (item, support) in locally_frequents:
        new_prefix = prefix + tuple(item)
        new_sdb = _project(sdb, new_prefix)
        _freq_seq(new_sdb, new_prefix, support, min_support,data_len, freq_seqs)


def _local_freq_items(sdb, prefix, min_support,data_len):
    items = defaultdict(int)
    freq_items = []
    for entry in sdb:
        visited = set()
        for element in entry:
            if element not in visited:
                items[element] += 1
                visited.add(element)
    # Sorted is optional. Just useful for debugging for now.
    for item in items:
        support = items[item]/float(data_len)
        if support >= min_support:
            freq_items.append((item, support))
    return freq_items


def _project(sdb, prefix):
    new_sdb = []
    if not prefix:
        return sdb
    current_prefix_item = prefix[-1]
    for entry in sdb:
        j = 0
        projection = None
        for item in entry:
            if item == current_prefix_item:
                projection = entry[j + 1:]
                break
            j += 1
        if projection:
            new_sdb.append(projection)
    return new_sdb

def process_results(freq_seqs, item_list):
    final_results = []    
    for result in freq_seqs:
        sequence = result[0]
        support = result[1]
        
        new_sequence = []
        for item in sequence:
            # convert letters to categories
            if item == 'a':
                item_name = item_list[0]
            elif item == 'b':
                item_name = item_list[1]
            elif item == 'c':
                item_name = item_list[2]
            elif item == 'd':
                item_name = item_list[3]
            elif item == 'e':
                item_name = item_list[4]
            elif item == 'f':
                item_name = item_list[5]
            elif item == 'g':
                item_name = item_list[6]
            elif item == 'h':
                item_name = item_list[7]
            elif item == 'i':
                item_name = item_list[8]
            elif item == 'j':
                item_name = item_list[9]
            elif item == 'k':
                item_name = item_list[10]
            elif item == 'l':
                item_name = item_list[11]
            elif item == 'm':
                item_name = item_list[12]
            elif item == 'n':
                item_name = item_list[13]
            elif item == 'o':
                item_name = item_list[14]
            elif item == 'p':
                item_name = item_list[15]
            elif item == 'q':
                item_name = item_list[16]
            new_sequence.append(item_name)
        
        new_sequence = tuple(new_sequence)
        final_results.append((new_sequence, support))
    
    return final_results
    
    
    
    
# %%
import time

t0 = time.clock()
print 'Start mining!'
filename = 'msnbc_mini.seq'
item_list = ['frontpage', 'news', 'tech', 'local', 'opinion', 'on-air', 'misc', 'weather', 'msn-news', 'health', 'living', 'business', 'msn-sports', 'sports', 'summary', 'bbs', 'travel']

# Load data
seqs = read_seq_file(filename)
load_t = time.clock()

# Mine for seqs
freq_seqs = freq_seq_enum(seqs, 0.2,len(seqs))
sorted(freq_seqs)
final_results = process_results(freq_seqs, item_list)
for result in final_results:
    print result
   
# Run statistics
mine_t = time.clock()
print 'Done mining!'
print '____________________________'
print '\n'

print 'Load data time = ', load_t-t0
print 'Mining time = ', mine_t-load_t
print 'Total time = ', mine_t-t0
print '\n'

import csv
import sys
import copy
import os
import argparse
from Word import Word
from Sentence import Sentence
from collections import Counter

csv.field_size_limit(sys.maxsize)


def read_file(infile):
    deprels = {}
    upos = {}
    feats = {}
    with open(infile, newline='') as r:
        csvreader = csv.reader(r, delimiter='\t')
        for row in csvreader:
            if len(row) >= 8:
                current_row = Word(row)
                if current_row.deprel() not in deprels:
                    deprels[current_row.deprel()] = 1
                else:
                    deprels[current_row.deprel()] += 1
                if current_row.upos() not in upos:
                    upos[current_row.upos()] = 1
                else:
                    upos[current_row.upos()] += 1
                for item in current_row.feats():
                    if item not in feats:
                        feats[item] = 1
                    else:
                        feats[item] += 1
    print("DEPRELS: ")
    print(len(deprels))
    print(deprels)
    print("UPOS: ")
    print(len(upos))
    print("FEATS: ")
    print(len(feats))


if __name__ == '__main__':
    read_file('conllu/squoia_qu.conllu')

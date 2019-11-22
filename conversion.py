import csv
import sys
import copy
import os
import argparse
from Word import Word
from Sentence import Sentence

csv.field_size_limit(sys.maxsize)


def read_file(infile, outfile):
    with open(infile, newline='') as r:
        csvreader = csv.reader(r, delimiter='\t')
        current_sentence = None
        for row in csvreader:
            if len(row) >= 1:
                if '# sent_id ' in row[0]:
                    if current_sentence:
                        write_sentence(current_sentence, outfile)
                    current_sentence = Sentence(row[0])
                elif '# text ' in row[0]:
                    current_sentence.set_text(row[0])
                elif len(row) >= 8:
                    converted_row = Word(row)
                    converted_row.convert()
                    current_sentence.append_word(converted_row)


def write_sentence(sentence, outfile):
    if not sentence.contains_quotes():
        to_write = sentence.to_rows()
        with open(outfile, 'a', newline='', encoding='utf-8') as o:
            csvwriter = csv.writer(o, delimiter='\t', lineterminator='\n')
            csvwriter.writerows(to_write)


def write_line(line, outfile):
    with open(outfile, 'a', newline='\n', encoding='utf-8') as w:
        csvwriter = csv.writer(w, delimiter='\t',  lineterminator='\n')
        csvwriter.writerow(line)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")
parser.add_argument(
    "-o", "--output", help="output file. default is <input file>.out")


def main():
    # python conversion.py -i conllu/test.conllu -o conversion_out/test.conllu
    args = parser.parse_args()
    INFILE = args.input
    if args.output:
        OUTFILE = args.output
    else:
        OUTFILE = INFILE + ".out"
    try:
        os.remove(OUTFILE)
    except:
        pass
    read_file(INFILE, OUTFILE)


if __name__ == '__main__':
    main()

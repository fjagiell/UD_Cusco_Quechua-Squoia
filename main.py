import os
import subprocess
import csv
import sys
import copy
import os
import argparse
from Word import Word
from Sentence import Sentence

csv.field_size_limit(sys.maxsize)


def read_file(infile):
    with open('conllu/' + infile, newline='') as r:
        csvreader = csv.reader(r, delimiter='\t')
        current_sentence = None
        for row in csvreader:
            if len(row) >= 1:
                if '# sent_id ' in row[0]:
                    if current_sentence:
                        write_sentence(current_sentence, infile)
                    current_sentence = Sentence(row[0])
                elif '# text ' in row[0]:
                    current_sentence._text_seg = row[0]
                elif len(row) >= 8:
                    converted_row = Word(row)
                    converted_row.convert()
                    current_sentence.append_word(converted_row)


def write_sentence(sentence, infile):
    if not sentence.contains_quotes():
        to_write = sentence.to_rows()
        with open('conllu_filtered/' + infile, 'a', newline='') as o:
            csvwriter = csv.writer(o, delimiter='\t')
            csvwriter.writerows(to_write)


def run_all(infile):
    IN_FILE = infile
    subprocess.run(['python', 'conversion.py', '-i', 'conllu_filtered/'+IN_FILE,
                    '-o', 'conversion_out/' + IN_FILE])
    subprocess.run(['grew', 'transform', '-grs', 'main.grs', '-i',
                    'conversion_out/' + IN_FILE, '-o', 'grew_out/' + IN_FILE])
    subprocess.run(['python', 'cleanup.py', '-all'])
    # subprocess.run(['column', '-t', 'cleanup_out/' + IN_FILE])


def main():
    IN_FILE = 'DW.conllu'
    OUTFILE = 'conllu_filtered/' + IN_FILE
    try:
        os.remove(OUTFILE)
    except:
        pass
    read_file(IN_FILE)
    run_all(IN_FILE)


if __name__ == '__main__':
    main()

import csv
import sys
import copy
import os
import argparse
from Word import Word

csv.field_size_limit(sys.maxsize)

# FILE = "conllu/test.conllu"
# OUTFILE = "conversion_out/test.conllu"


def read_file(file, outfile):
    with open(file, newline='') as r:
        csvreader = csv.reader(r, delimiter='\t')
        for row in csvreader:
            if len(row) >= 1:
                if "# text" in row or "# sent_id" in row:
                    write_line(row, outfile)
                elif len(row) > 8:
                    converted_row = Word(row)
                    write_line(converted_row.to_row(), outfile)
            else:
                write_line([], outfile)


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

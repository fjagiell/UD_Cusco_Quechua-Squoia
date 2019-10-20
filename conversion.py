import csv
import sys
import copy
import os
from Word import Word

csv.field_size_limit(sys.maxsize)

FILE = "conllu/test.conllu"
OUTFILE = "conversion_out/test.conllu"


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


def generate_textline(rows):
    text = list(map(lambda x: x[1], rows[3:]))
    # print(" ".join(text))
    return ["# text = " + " ".join(text)]


def main():
    try:
        os.remove(OUTFILE)
    except:
        pass
    read_file(FILE, OUTFILE)


if __name__ == '__main__':
    main()

import os
import csv
from Word import Word
import conversion
from Sentence import Sentence
import argparse

# TO DO:
# SpaceAfter=No if there is no space after it
# alphabetize features


def clean_it(f, write_to_file):
    if write_to_file:
        filename = f.split("/")[-1]
        write_file = "cleanup_out/" + filename
        try:
            os.remove(write_file)
        except:
            pass
    else:
        write_file = ""
    sentence = None
    with open(f, newline='') as r:
        csvreader = csv.reader(r, delimiter='\t')
        for row in csvreader:
            if len(row) >= 8:
                converted_row = Word(row)
                converted_row.cleanup()
                sentence.append_word(converted_row)
            elif len(row) > 0:
                if "# sent_id = " in row[0]:
                    if sentence:
                        finish_sentence(sentence, write_file)
                    sentence = Sentence(row[0])
                elif "# text = " in row[0]:
                    sentence.set_seg(row[0])
            else:
                if write_to_file:
                    conversion.write_line(row, write_file)
        if sentence:
            finish_sentence(sentence, write_file)


def finish_sentence(sentence, f):
    # sentence.cleanup_punct()
    if f == "":
        pass
    else:
        conversion.write_line([sentence.id()], f)
        conversion.write_line([sentence.seg()], f)
        conversion.write_line([sentence.sentence_converted()], f)
        for word in sentence.words():
            conversion.write_line(word.to_row(), f)


parser = argparse.ArgumentParser()
parser.add_argument("-all", default=False, action="store_true",
                    help="runs through all files in grew_out and places results in cleanup_out")


def main():
    args = parser.parse_args()
    directory = os.fsencode("grew_out/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".conllu"):
            clean_it("grew_out/" + filename, args.all)


if __name__ == '__main__':
    main()

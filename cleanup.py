import os
import csv
from Word import Word
import conversion
from Sentence import Sentence


def remove_xpos(line):
    line[4] = "_"
    return line


def clean_it(f):
    filename = f.split("/")[-1]
    write_file = "cleanup_out/" + filename
    try:
        os.remove(write_file)
    except:
        pass
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
                conversion.write_line(row, write_file)
        if sentence:
            finish_sentence(sentence, write_file)


def finish_sentence(sentence, f):
    conversion.write_line([sentence.id()], f)
    conversion.write_line([sentence.seg()], f)
    sentence_converted = calc_sentence(sentence)
    conversion.write_line([sentence_converted], f)
    for word in sentence.words():
        conversion.write_line(word.to_row(), f)


def calc_sentence(sentence):
    full_sentence = ["# text ="]
    for word in sentence.words():
        full_sentence.append(word.form())
    return " ".join(full_sentence)


def main():
    directory = os.fsencode("grew_out/")
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".conllu"):
            clean_it("grew_out/" + filename)
        else:
            continue


if __name__ == '__main__':
    main()

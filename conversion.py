import csv
import sys
import copy
import os

csv.field_size_limit(sys.maxsize)

FILE = "conllu/squoia_sample.conllu"
OUTFILE = "out/squoia_sample_out.conllu"

deprel = {
    "arg": "@obl:arg",
    "aux": "@aux",
    "ben": "@obl:ben",
    "caus": "@obl:caus",
    "co": "@conj",
    "iobj": "@iobj",
    "adv": "@advmod",
    "punc": "@punct",
    "r.disl": "@dislocated",  # ?
    "src": "@obl:src",
    "loc": "@nmod:loc",  # @obl:loc
    "subj": "@csubj",  # @usubj
    "acmp": "@nmod",  # @obl
    "mod": "@nmod",  # @obl, @advmod
}

feats = {
    "+Abl": "Case=Abl",
    "+Acc": "Case=Acc",
    "+Add": "Case=Add",
    "+Ben": "Case=Ben",
    "+Caus": "Voice=Caus",
    "+Dat": "Case=Dat",
    "+Dim": "Deriv=Dim",
    "+Fut": "Tense=Fut",
    "+Gen": "Case=Gen",
    "+Hab": "Tense=Past|Aspect=Hab",
    "+Imp": "Mood=Imp",
    "+Instr": "Case=Ins",
    "+Ipst": "Tense=Past|Evident=Sqa",
    "+Loc": "Case=Loc",
    "+Perf": "Aspect=Perf",
    "+Pres": "Tense=Pres",
    "+Prog": "Aspect=Prog",
    "+Pst": "Tense=Past",
    "+Rflx": "Reflexive=Yes",
    "+Sg": "Number=Sing"
}


def read_file(file, outfile):
    with open(file, newline='') as r:
        csvreader = csv.reader(r, delimiter='\t')
        current_sentence = []
        for row in csvreader:
            if len(row) >= 1:
                converted_row = copy.deepcopy(row)
                if "# sent_id " in row[0]:
                    if len(current_sentence) > 2:
                        write_sentence(current_sentence, outfile)
                    current_sentence = [row]
                elif "# text " in row[0]:
                    text = copy.deepcopy(row[0])
                    parts = text.split("=")
                    row[0] = "# text[seg] =" + parts[1]
                    current_sentence.append(row)
                    current_sentence.append(["# text = "])
                else:
                    if len(row) > 6:  # if is a sentence row
                        features = row[5].split("|")
                        new_features = []
                        for feat in features:
                            if feat in feats:
                                new_features.append(feats[feat])
                            else:
                                new_features.append(feat)
                        converted_row[5] = "|".join(new_features)
                        if len(row[5]) > 1:
                            converted_row[-1] = "feats:[" + row[5] + "]"
                    current_sentence.append(converted_row)


def write_sentence(sentence, outfile):
    sentence.append([])
    with open(outfile, 'a', newline='') as w:
        csvwriter = csv.writer(w, delimiter='\t')
        print(sentence)
        csvwriter.writerows(sentence)


def generate_textline(rows):
    text = list(map(lambda x: x[1], rows[3:]))
    print(" ".join(text))
    return ["# text = " + " ".join(text)]


def main():
    try:
        os.remove(OUTFILE)
    except:
        pass
    read_file(FILE, OUTFILE)


if __name__ == '__main__':
    main()

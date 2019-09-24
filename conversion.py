import csv
import sys
import copy

csv.field_size_limit(sys.maxsize)

FILE = "conllu/squoia_qu.conllu"
OUTFILE = "out/squoia_qu_out.conllu"

deprel = {
    "arg": "@obl:arg",
}

# need to update sentence at the top
# update numberings

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
                if "# sent_id " in row[0]:
                    current_sentence.append(["\n"])
                    write_sentence(current_sentence, outfile)
                    current_sentence = [row]
                converted_row = row
                if len(row) > 6:  # if is a sentence row
                    features = row[5].split("|")
                    new_features = []
                    for feat in features:
                        if feat in feats:
                            new_features.append(feats[feat])
                        else:
                            new_features.append(feat)
                    converted_row[5] = "|".join(new_features)
                    if (should_attach_suffix(row)):
                        if len(current_sentence) > 0:
                            converted_row = copy.deepcopy(
                                merge_rows(converted_row,
                                           current_sentence.pop()))
                current_sentence.append(converted_row)


def write_sentence(sentence, outfile):
    with open(outfile, 'a', newline='') as w:
        csvwriter = csv.writer(w, delimiter='\t')
        csvwriter.writerows(sentence)


def should_attach_suffix(row):
    if row[1][0] == "-":
        if row[7] == "ns":
            return True
    return False


def merge_rows(next_row, prev_row):
    merged_features = set(next_row[5].split("|"))
    for feature in prev_row[5].split("|"):
        merged_features.add(feature)
    new_row = copy.deepcopy(prev_row)
    new_row[1] = prev_row[1] + next_row[1][1:]
    new_row[5] = "|".join(merged_features)
    if len(new_row[9]) > 1:
        new_row[9] += "|Merged=True"
    else:
        new_row[9] = "Merged=True"
    return new_row


def main():
    read_file(FILE, OUTFILE)


if __name__ == '__main__':
    main()
import csv
import argparse


def read_file(infile):
    with open(infile, 'r') as r:
        line1 = []
        line2 = []
        depedges = []
        csvreader = csv.reader(r, delimiter='\t')
        for row in csvreader:
            if not '# ' in row[0][:3] and not '-' in row[0]:
                row[1] = row[1].replace('$', '\\$').replace('_', '\\_')
                row[3] = '{\\tt ' + \
                    row[3].replace('$', '\\$').replace('_', '\\_') + '}'
                line1.append(row[1])
                line2.append(row[3])
                if not row[6] == '0':
                    depedges.append([row[6], row[0], row[7]])
        print('\\scalebox{0.5}{')
        print('\\begin{dependency}')
        print('\\begin{deptext}[column sep=0.1cm]')
        print(' \\& '.join(line1) + '\\\\')
        print(' \\& '.join(line2) + '\\\\')
        print('\\end{deptext}')
        for i in range(len(depedges)):
            print('\\depedge{' + str(depedges[i][0]) + '}{' +
                  str(depedges[i][1]) + '}{' + depedges[i][2] + '}')
        print('\\end{dependency}')
        print('}')


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")


def main():
    # python maketree.py -i conllu/test.conllu
    args = parser.parse_args()
    INFILE = args.input
    read_file(INFILE)


if __name__ == '__main__':
    main()

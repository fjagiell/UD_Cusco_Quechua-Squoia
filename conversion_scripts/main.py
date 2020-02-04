import os
import subprocess
import csv
import sys
import copy
import os
import argparse

'''
takes an input file, runs it through conversion.py, then grew (using main.grs), then cleanup.py

(currently assumes the input is squoia_qu.conllu)
'''


def run_all(infile):
    IN_FILE = infile
    subprocess.run(['python3', 'conversion.py', '-i', 'conllu/'+IN_FILE,
                    '-o', 'conversion_out/' + IN_FILE])
    subprocess.run(['grew', 'transform', '-grs', 'main.grs', '-i',
                    'conversion_out/' + IN_FILE, '-o', 'grew_out/' + IN_FILE])
    subprocess.run(['python3', 'cleanup.py', '-all'])
    # subprocess.run(['column', '-t', 'cleanup_out/' + IN_FILE])


def main():
    IN_FILE = 'squoia_qu.conllu'
    OUTFILE1 = 'conversion_out/' + IN_FILE
    OUTFILE2 = 'cleanup_out/' + IN_FILE
    try:
        os.remove(OUTFILE1)
    except:
        pass
    try:
        os.remove(OUTFILE2)
    except:
        pass
    run_all(IN_FILE)


if __name__ == '__main__':
    main()

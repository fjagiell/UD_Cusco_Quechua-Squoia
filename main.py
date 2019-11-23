import os
import subprocess
import csv
import sys
import copy
import os
import argparse


def run_all(infile):
    IN_FILE = infile
    subprocess.run(['python', 'conversion.py', '-i', 'conllu/'+IN_FILE,
                    '-o', 'conversion_out/' + IN_FILE])
    subprocess.run(['grew', 'transform', '-grs', 'main.grs', '-i',
                    'conversion_out/' + IN_FILE, '-o', 'grew_out/' + IN_FILE])
    subprocess.run(['python', 'cleanup.py', '-all'])
    # subprocess.run(['column', '-t', 'cleanup_out/' + IN_FILE])


def main():
    IN_FILE = 'DW.conllu'
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

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
    subprocess.run(['column', '-t', 'cleanup_out/' + IN_FILE])


def main():
    IN_FILE = 'DW.conllu'
    OUTFILE = 'conversion_out/' + IN_FILE
    try:
        os.remove(OUTFILE)
    except:
        pass
    run_all(IN_FILE)


if __name__ == '__main__':
    main()

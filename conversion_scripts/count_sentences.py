import sys
import fileinput

'''
reads output of validate.py and counts number of sentences with reported violations
'''

if __name__ == '__main__':
    sentences = set()
    for line in fileinput.input():
        if '***' in line[:5].rstrip():
            break
        else:
            try:
                chunks = line.split('[')
                words = chunks[1].split(' ')
                sent = words[3]
                sent = sent.replace(']', '').replace(':', '')
                sent = sent.strip()
                sentences.add(sent)
            except:
                pass
    print(len(sentences))
    print(sentences)
    print(len(sentences)/1979)
    print(str(len(sentences)))

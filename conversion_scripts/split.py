import sys
import random

trees = sys.stdin.read().split('\n\n')
batch = int(len(trees)/10)

random.shuffle(trees)

prefix = './splits/'

i = 0
for part in range(0, len(trees)-batch, batch):
    f = open(prefix + '%2d % )
    f.write('\n\n'.join(trees[part:part+batch]))
    print(i, part)
    f.close()
    i += 1

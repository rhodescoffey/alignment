"""
    Quick script to display results of vowel extraction

"""

from glob import glob
from phonemes import VOWELS
import sys

PATH = "./sounds/*"

def make_vowel_file(duration, lang):
    total = 0
    zero = 0
    one = 0
    greater = 0
    vf = open('vowel_results.txt', 'a+')
    header = 'Limit: {}\n'.format(str(duration))
    vf.write(header)
    for v in VOWELS[lang]:
        vc = 0
        for f in glob(PATH):
            if f[9] == v:
                vc += 1
        total += vc
        if vc == 0:
            zero += 1
        elif vc == 1:
            one += 1
        else:
            greater += 1
        s = '{0}: {1}\n'.format(v, str(vc))
        vf.write(s)
    fin = '\nTotal: {0}\n0 Entries: {1}\n1 Entry: {2}\n>1 Entry: {3}\n'
    fin = fin.format(str(total), str(zero), str(one), str(greater))
    vf.write(fin)
    vf.close()


if "__name__" == "__main__":
    make_vowel_file(sys.argv[1], sys.argv[2])

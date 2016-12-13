"""
    aligner.py

    This program is for the comparison of aligned strings taken from utterances
    stored in TextGrid format. All files in a given directory are subject to
    Levenshtein distance comparison in all pairwise combinations, and organized
    into a .csv file, with data format:

    *** File 1, Ann 1, Phonemes, Time, File 2, Ann 2, Phonemes, Time ***

    Functions: check_sig(txt, ann)- checks file name for annotator's name
               utter_comp(tg, s)- aligns original phonemes in TextGrid with
                                  aligned string from LD
               make_utter_table(lang, min, max)- utter_comp() on all files in a
                                                 directory; output to .csv

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 7/29/15

"""

import sys
import csv
from tg import *
from align_funcs import *
from glob import glob
from itertools import combinations
from phonemes import FILE_HEADERS, SIGNATURES

""" Open files in utf-8 by default """
reload(sys)
sys.setdefaultencoding('utf-8')


def check_sig(txt, ann):
    """ Looks for annotator's signature, taken from list, in given string """

    for i in ann:
        if i in txt:
            return i
    return 'orig'


def time_align(tg, s):
    """ Matches aligned string with the times gives in the TG """

    d = []  # returns list of tuples
    i = 0  # iterator
    s_adj = 0  # steps forward in aligned string
    tg_adj = 0  # steps forward in tg string

    """ Until end of TG is reached """
    while (i + tg_adj) < len(tg.phon):
        #  *Uncomment to debug*  print s, tg.phon, s[i+s_adj], tg.tiers[i].phon
        if (s[i+s_adj] != tg.tiers[i].phon and 
            is_diff(s[i+s_adj], tg.tiers[i+tg_adj].phon)):
            tg_adj += 1
        elif s[i+s_adj] != '_':
            d.append((s[i+s_adj], tg.tiers[i+tg_adj].xmin))
            i += 1
        else:
            d.append(('_', 'NA'))
            s_adj += 1
    return d


def make_utter_table(lang, mini, maxi):
    """ Creates table of utterance comparisons of all files in a directory """

    path = FILE_HEADERS[lang]
    d = [('File1', 'Ann1', 'Ann1 Phoneme', 'Ann1 Time',
          'File2', 'Ann2', 'Ann2 Phoneme', 'Ann2 Time')]

    for i in range(mini, maxi):
        antns = []  # Holds strings for ED
        names = []  # Holds names of anntor's for strings in l
        tgs = []  # Holds TG's for time series alignment

        """ Loop through directory by utterance number """
        for fi in glob(path + '*' + str(i) + '*'):
            j = TextGrid(fi, lang)
            antns.append(j.phon)
            names.append(check_sig(fi, SIGNATURES[lang]))
            tgs.append(j)

        """ Find all possible ED comparisons of transcriptions """
        for k, l, m in zip(combinations(antns, 2), combinations(names, 2),
                           combinations(tgs, 2)):
            grid, s1, s2, dist = alignment(*k)
            try:
                ann_one = time_align(m[0], s1)
                ann_two = time_align(m[1], s2)
            except IndexError:
                print "TextGrid improperly annotated, cannot parse."
                raise
            for i, j in zip(ann_one, ann_two):
                d.append(((m[0].name,) + (l[0],) + i + (m[1].name,) + (l[1],) +
                           j))

    with open("Ann_Alignment_" + str(mini) + "_" + str(maxi) + ".csv", "w") as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerows(i for i in d)


if __name__ == '__main__':
    make_utter_table(str(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

”””
    sound_extract.py

    This program sifts through annotator data in the Excel file and extracts
    vowels that are most agreed upon by annotators. Once these vowels are found
    their time intervals are extracted and output.

    The extraction is based off of an Excel file with headers:
    File 1, Ann1, Ann1_Phoneme, Ann1_Time, File2, Ann2, Ann2_Phoneme, Ann2_Time
    Magic numbers correspond to the indices of these headers (i.e. 0-7)

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 7/30/15

"""

import csv
import subprocess
from glob import glob
import re
import sys
from phonemes import VOWELS


PATH = "./sound_files/Ch9_BabyC_3__" #  Extract from current directory
WAV = ".wav" #  Output file extension
LIM = 0.1 #  Minimum duration for extracted vowels

def find_phon(lang, file):
    pad = 0.01 #  Padding for vowel extraction
    sounds = []
    with open(file, 'r') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            for phon in VOWELS[lang]:
                if row[2] == phon and row[6] == phon:
                    end = next(data)
                    avg_st = (float(row[3]) + float(row[7]))/2.0 - pad
                    if end[3] == 'NA':
                        avg_end = float(end[7]) + pad
                    elif end[7] == 'NA':
                        avg_end = float(end[3]) + pad
                    else:
                        avg_end = (float(end[3]) + float(end[7]))/2.0 + pad
                    dur = avg_end - avg_st
                    if dur > LIM:
                        sounds.append((phon, row[0], row[4], str(avg_st), str(dur)))
    return sounds


def sound_extract(sounds):
    file_id = '\d{4}'
    global PATH
    global WAV
    for i in sounds:
        c = 0
        m = re.findall(file_id, i[1])
        for wav in glob(PATH + '*' + '.wav'):
            if m[0] in wav:
                c += 1
                out = i[0] + m[0] + '_' + str(c) + WAV
                s = ['sox', wav, out, 'trim', i[3], i[4]]
                subprocess.call(s)


if __name__ == '__main__':
    sound_extract(find_phon(str(sys.argv[1]), sys.argv[2]))

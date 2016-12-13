"""
    tg.py

    Classes for extracting data from TextGrid files.

    Classes: TextGrid(object)- TextGrid file data
             Tier(object)- Phonemic data from intervals in TextGrid class

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 7/14/15

"""

import re
import codecs
from phonemes import MAPPING, NOISE


class TextGrid(object):
    """ Extracts meaningful data from TextGrids """
    def __init__(self, file, lang):
        self.name = str(file)  # File name
        self.data = self._read_tg(file)  # Extracts TG data
        self.type = self._find_type(self.data)  # Short file or reg file
        self.size = float(re.findall('\d+', self.data[6])[0])  # Num of tiers
        self.xmin = float(re.findall('\d+.\d+', self.data[3])[0])  # Start
        self.xmax = float(re.findall('\d+.\d+', self.data[4])[0])  # End
        self.tiers = self._form_tiers()  # Organizes data into tiers
        self.phon = self._phonemes(lang)  # Utterance in data (str)

    def __iter__(self):
        """ TD is iterable """
        return iter(self.tiers)

    def replace_all(self, txt, dic):
        """ Mapping function for phonemes """
        for i, j in dic.iteritems():
            txt = txt.replace(i, j)
        return txt

    def _read_tg(self, filename):
        """ Attempts to open and access data in TextGrid file """
        try:
            f = codecs.open(filename, encoding='utf-16').readlines()
        except:
            f = codecs.open(filename, encoding='utf-8').readlines()
        return f

    def _find_type(self, filedata):
        """ Determines whether or not file is long or short format """
        if "short" in filedata[0]:
            return "short"
        else:
            return "reg"

    def _form_tiers(self):
        """ Organizes data from TG into tiers """
        inum = []

        for i, line in enumerate(self.data):
            if len(inum) > 1:
                break
            if "IntervalTier" in line:
                inum.append(i)

        end = inum[1]
        if self.type == 'short':
            start = inum[0] + 5
            itvl = 3
        else:
            start = inum[0] + 6
            itvl = 4

        tiers = []
        nums = r'\d+.\d+'
        wds = r'"(.*)"'
        sv = r'(?<=.)\(.\)$'

        for i in range(start, end, itvl):
            min = float(re.findall(nums, self.data[i])[0])
            max = float(re.findall(nums, self.data[i+1])[0])
            ph = str(re.findall(wds, self.data[i+2])[0]).strip(NOISE)
            ph = re.sub(sv, '', ph) #  sr keeps adding (*) past 8513
            if ph == '':
                ph = '-'
            t = Tier(min, max, ph)
            tiers.append(t)

        return tiers

    def _phonemes(self, lang):
        """ Isolates and formats TG phonemic data for alignment
            See phonemes.py for list of phonemes """
        text = ''

        for i in self.tiers:
            entry = i.phon
            text += entry

        text = self.replace_all(text, MAPPING[lang][0])
        text = self.replace_all(text, MAPPING[lang][1])
        return text


class Tier(object):
    """ Each annotated phoneme and its duration in TG """
    def __init__(self, xmin, xmax, phon):
        self.xmin = xmin
        self.xmax = xmax
        self.phon = phon

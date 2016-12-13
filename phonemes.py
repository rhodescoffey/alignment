""" List of phonetic symbols used in Annotation 

    Changes to Mandarin: (@) --> 1
                         (&) --> 2
                         (a) --> 3 *diphthongs*
                         sp --> - *silence*
                         --> | *no annotation* 

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 7/15/15

"""

SPAN_MLTI = { 'laugh': '!', 'AA1': 'A', 'CH': 'C', 'DH': 'D', 'EY1': 'E',
              'HH': 'h', 'IY1': '1', 'OW1': 'O', 'TH': 'T', 'UW1': 'U', 
              'lg': '!', 'sil': '-', 'sp': '-', '{LG}': '!', '{SL}': '-', 
              'gl': '!', '{GL}': '!', 'BH': 'v', 'LG': '!' }
SPAN_SG = { 'B': 'b', 'D': 'd', 'F': 'f', 'G': 'g', 'K': 'k', 'L': 'l',
            'M': 'm', 'N': 'n', 'P': 'p', 'R': 'r', 'S': 's', 'T': 't', 
            'V': 'v', 'W': 'w', 'Y': 'y', 'Z': 'z' }
CHIN_MLTI = { 'laugh': '!', '(silent)': '-' }
CHIN_SG = { '(@)': '1', '(&)': '2', '(a)': '3', 'lg': '!',
             'sil': '-', 'sp': '-', '{LG}': '!', '{SL}': '-', 'gl': '!',
             '{GL}': '!', 'ns': '-' }

MAPPING = { 'CHIN': (CHIN_MLTI, CHIN_SG), 'SPAN': (SPAN_MLTI, SPAN_SG) }
CONSONANTS = { 'CHIN': 'bpmdtlngkhNzcsjqxrZCSfywW-|!',
               'SPAN': 'bCdDfghklmnprstTvwyz!-|' }
VOWELS = { 'CHIN': 'iI%eEU&a@o>uR123V', 'SPAN': 'AEIOU' }
SIGNATURES = { 'CHIN': ['JL', 'srds', 'cl_sr', 'sr', 'kx', 'hy', 'YP', 'dy',
               'xj'], 'SPAN': ['jc', 'ca'] }
FILE_HEADERS = { 'CHIN': './CHIN_TG/Ch9_BabyC_3__', 'SPAN': './SPAN_TG/01b_' }
NOISE = ' ~^?*'

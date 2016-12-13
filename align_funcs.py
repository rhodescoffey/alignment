"""
    align_funcs.py

    The alignment algorithm takes in TextGrid classes and extracts meaningful
    data. This information consists of the beginning of a phoneme's utterance,
    its end, and its phonemic transcription. With this information the program
    finds the edit distance between two given utterances, phoneme by phoneme.

    Functions: is_vow(char)- Checks if char is vowel
               is_cons(char)- Checks if char is consonant
               alignment(s1, s2)- Performs LD on two TextGrids

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 7/28/15

"""

import numpy as np
from phonemes import VOWELS, CONSONANTS


def is_vow(char):
    """ Checks if char is vowel """

    for i in VOWELS.values():
        if char in i:
            return True
    else:
        return False


def is_con(char):
    """ Checks if char is consonant """

    for i in CONSONANTS.values():
        if char in i:
            return True
    else:
        return False


def is_diff(char1, char2):
    """Checks if char are different, i.e. vow/vow, cons/cons, or vow/cons"""

    if (is_con(char1) and is_vow(char2)) or (is_vow(char1) and is_con(char2)):
        return True

    else:
        return False


def alignment(s1, s2):
    """ Minimum number of edits needed to get from one string to another """
    """ Wikipedia: Levenshtein distance: Computing Levenshtein distance """

    grid = [[0 for x in range(len(s2) + 1)] for x in range(len(s1) + 1)]
    backtrace = [[0 for x in range(len(s2) + 1)] for x in range(len(s1) + 1)]

    for i, item in enumerate(grid):
        grid[i][0] = i
    for j, jtem in enumerate(grid[0]):
        grid[0][j] = j
    for i in range(1, len(grid)):
        for j in range(1, len(grid[0])):
            if s1[i-1] == s2[j-1]:
                cost = 0
            elif is_diff(s1[i-1], s2[j-1]):
                cost = 2
            else:
                cost = 1

            funcs = [(grid[i-1][j] + 1), (grid[i][j-1] + 1),
                     (grid[i-1][j-1] + cost)]

            grid[i][j] = min(funcs)
            backtrace[i][j] = np.argmin(funcs)

    """ Backtrace function """
    a1 = ""
    a2 = ""
    i = len(backtrace)-1
    j = len(backtrace[0])-1

    """ Loop through point array to find cheapest operation """
    while (i != 0) and (j != 0):
        if backtrace[i][j] == 2:  # Substitution
            a1 += s1[i-1]
            a2 += s2[j-1]
            i -= 1
            j -= 1

        elif backtrace[i][j] == 1:  # Deletion
            a1 += '_'
            a2 += s2[j-1]
            j -= 1

        else:  # Insertion
            a1 += s1[i-1]
            a2 += '_'
            i -= 1

    a1 = a1[::-1]
    a2 = a2[::-1]

    return grid, a1, a2, grid[len(grid)-1][len(grid[0])-1]

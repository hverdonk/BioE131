#!/usr/bin/python

"""

Needleman-Wunsch Aligner
Bioengineering 131/231, Fall 2018

Command-line script to read in the contents of a multi-FASTA containing two
sequences and a score matrix, perform a global alignment, and print the
resulting alignment matrix and optimal alignment to STDOUT.

"""

import os
import sys

class NWAligner:
    def __init__(self, score_matrix_fname):
        self.score_matrix, self.gap_penalty = self.load_score_matrix(score_matrix_fname)

    @staticmethod
    def load_score_matrix(fname):
        """
        Input: (String) A path to a scoring matrix file.
        Output: (Dictionary) A nested dictionary where keys are strings
                and elements are scores as integers.
    
        Example:
    
        >>> matrix, gap_penalty = NWAligner.load_score_matrix('/home/bioe131/BLOSUM62')
        >>> matrix['A']['A']
        4
        >>> matrix['W']['W']
        11
        >>> gap_penalty
        -4

        """

        score_matrix = {}
        gap_penalty = None
        keys = []

        with open(fname) as fp:
            for line_num, line in enumerate(fp):
                # ignore comments in matrix file and trailing empty lines
                if line.startswith("#") or (len(line.split()) == 0):
                    continue
                ## BEGIN MY WORK ##
                elif len(line.strip().split()) == 1:
                    gap_penalty = int(line.strip())
                elif (line_num == 0):
                    keys = line.strip().split()
                    for mainkey in keys:
                        score_matrix[mainkey] = {}
                else:
                    values = [int(x) for x in line.strip().split()]
                    mainkey = keys[line_num - 1]
                    score_matrix[mainkey] = dict(zip(keys, values))
                ## END MY WORK ##

                ### TODO ###
                # Parse matrix file line-by-line and load into nested dictionaries.
                #
                # Last line of matrix contains the gap penalty which must be pulled
                # out and returned.

        return score_matrix, gap_penalty

    @staticmethod
    def load_FASTA(fname):
        """
        Input: (String) A path to a FASTA file containing exactly two sequences.
        Output: (List) A list containing two strings: one for each sequence.

        Example:

        >>> seqs = NWAligner.load_FASTA('example.fa')
        >>> seqs[0]
        'YAADSKATPGNPAFHQDEIFLARIAFIYQMWDGGQLKLIDYAPHHVMCEE'
        >>> seqs[1]
        'WVGQPNMKVQHWSNMKACCVKFITWTFIAPEKHACKWTETAYQADCDIIW'
        >>> len(seqs)
        2

        """

        seqs = []

        ### TODO ###
        # Load FASTA file and return list of sequences.
        # Throw an error if there are more than two sequences in the file.
        with open(fname) as fp:
            for line_num, line in enumerate(fp):
                # ignore comments in matrix file and trailing empty lines
                if (len(line.split()) == 0):
                    continue
                elif (line_num > 3):
                    print('Error: More than two sequences provided.')
                    sys.exit(1)
                elif (line_num%2 == 1):
                    seqs.append(line.strip())
                #rstrip removes trailing newlines

        return seqs

    def align(self, seq_x, seq_y, print_matrix = False):
        """
        Input: (Strings) Two sequences to be aligned (seq_x and seq_y).
               (Boolean) If print_matrix is True, print the dynamic programming
                         matrix before traceback.
        Output: (Tuple of strings) Two sequences, aligned.

        Example:

        >>> aligner = NWAligner('BLOSUM62')
        >>> seqs = aligner.load_FASTA('example.fa')
        >>> aligner.align(seqs[0], seqs[1])
        ('YAAD-SKATPGNPAF---HQDEIF--L-AR--IA-FIYQM-WDGGQLK-LIDYAPH-HVM-C---E-------E---',
         'W---VGQ--P-N--MKVQH----WSNMKA-CCV-KFI---TW------TFI--APEKH--ACKWTETAYQADCDIIW')

        """

        ###
        ### INITIALIZATION
        ###

        # create two empty matrices with sizes based on the input sequences.
        # one contains the dynamic programming matrix, the other contains
        # pointers we'll use during traceback
        matrix = [[0] * (len(seq_y) + 1) for _ in range(len(seq_x) + 1)]
        pointers = [[0] * (len(seq_y) + 1) for _ in range(len(seq_x) + 1)]

        ### TODO ###
        matrix[0][0] = 0

        # Fill the top row of the matrix with scores for gaps.
        for i in range(1, len(seq_x) + 1):
            matrix[i][0] = matrix[i-1][0] + self.gap_penalty
            pointers[i][0] = 'left'

        # Fill the first column of the matrix with scores for gaps.
        for j in range(1, len(seq_y) + 1):
            matrix[0][j] = matrix[0][j-1] + self.gap_penalty
            pointers[0][j] = 'up'
        

        ###
        ### RECURSION
        ###

        # fill the dynamic programming and pointer matrices
        for x in range(1, len(seq_x) + 1):
            for y in range(1, len(seq_y) + 1):
                match_score = self.score_matrix[seq_x[x - 1]][seq_y[y - 1]]

                ### TODO ###
                # Take the maximum score of three possibilities:
                #   1) The element in the matrix diagonal from this one
                #      plus the score of an exact match
                #   2) The element to the left plus a gap penalty
                #   3) The element above plus a gap penalty
                # ... and set the current element (matrix[x][y]) equal to that
                #
                # Keep track of which of these choices you made by setting
                #   the same element (i.e., pointers[x][y]) to some value that
                #   has meaning to you.

                above_score = matrix[x][y-1] + self.gap_penalty
                left_score = matrix[x-1][y] + self.gap_penalty
                diagonal_score = matrix[x-1][y-1] + match_score

                max_score = max(above_score, left_score, diagonal_score)
                matrix[x][y] = max_score

                if max_score == diagonal_score:
                    pointers[x][y] = 'diagonal'
                elif max_score == left_score:
                    pointers[x][y] = 'left'
                else:
                    pointers[x][y] = 'up'
                

        # print the dynamic programming matrix
        if print_matrix:
            for x in range(len(seq_x) + 1):
                print(" ".join(map(lambda i: str(int(i)), matrix[x])))

        ###
        ### TRACEBACK
        ###

        # starting from the bottom right corner, follow the pointers back
        x, y = len(seq_x), len(seq_y)

        # fill these lists with the aligned sequences
        align_x = []
        align_y = []

        ### TODO ###
            # Follow pointers back through the matrix to the origin.
            # Depending on which "move" you made at each element in the
            #   matrix, you'll either align seq_x to seq_y, seq_x to a gap, or
            #   seq_y to a gap.

        while x > 0 or y > 0:
            move = pointers[x][y]
            if move == 'up':
                #seq x gap (x stays constant, y changes)
                align_x.append('-')
                align_y.append(seqs[1][y-1])
                y-=1
            elif move == 'left':
                #seq y gap (y stays constant, x changes)
                align_x.append(seqs[0][x-1])
                align_y.append('-')
                x-=1
            else:
                align_x.append(seqs[0][x-1])
                align_y.append(seqs[1][y-1])
                x-=1
                y-=1


        # flip the alignments, as they're reversed
        return ("".join(align_x[::-1]), "".join(align_y[::-1]))

###                                      ###
### NO NEED TO EDIT CODE BELOW THIS LINE ###
###                                      ###

if __name__ == '__main__':
    def usage():
        print('usage: %s matrixfilename stringfilename')
        sys.exit(1)

    if len(sys.argv) != 3:
        usage()

    for fname in sys.argv[1:]:
        if not os.path.isfile(fname):
            print('Can not open %s' % (fname,))
            usage()

    aligner = NWAligner(sys.argv[1])
    seqs = aligner.load_FASTA(sys.argv[2])
    result = aligner.align(seqs[0], seqs[1])

    print('>seq1\n%s\n>seq2\n%s' % (result[0], result[1]))

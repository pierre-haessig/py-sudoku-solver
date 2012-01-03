#!/usr/bin/python
# -*- coding: UTF-8 -*-
""" Solving test of the sudoku_solver program

It attempts to solve all the games placed in the "sudoku-example" directory
Pierre Haessig — January 2012
"""

from __future__ import print_function
from glob import glob

from sudoku_solver import Sudoku

sudoku_games = glob('./sudoku-examples/sudoku-*.txt')
sudoku_games.sort()

successes = 0
for game in sudoku_games:
    S = Sudoku(game)
    (is_solved, nb_iter) = S.solve_game()
    if all([len(c.possibilities)==9 for c in S.cells]):
        print(' (this was an empty Sudoku)')
        successes += 1 # count it as a success anyway
    else:
        successes += int(is_solved)
    print('-'*50)

print('\nTest ran without failure')
print('Number of successes : %d/%d' % 
      (successes, len(sudoku_games)))

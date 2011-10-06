=============
Sudoku Solver
=============

A quick hobby Python program to represent
and (attempt to) solve the classic Sudoku game

Example
-------

You can run the program onto an example Sudoku grid file::

    $ python sudoku-solver.py ./sudoku-examples/sudoku-level4-1.txt

Grid files are just plain text files describing the grid in terms
of the cell content. Empty cells are marked by anything but a number 
(good option is to use a "-" for example)::

    $ cat ./sudoku-examples/sudoku-level4-1.txt 
    ----3-596
    --91-----
    -754-----
    36--2----
    8-------2
    ----6--47
    -----516-
    -----83--
    924-1----


Copyright © Pierre Haessig - October 2011
This program is available for free, under the BSD license 

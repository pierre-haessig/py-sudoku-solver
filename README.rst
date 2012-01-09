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

Some References
---------------
 * Great article about solving Sudoku in Python : 
   http://norvig.com/sudoku.html Very lean approach
   I didn't go always the same way, but main ideas are similar. 
   I also put more Object Orientation than he does in my code
 * The sparse1 example (only 17 solved cells to start with) :
   http://passeurdesciences.blog.lemonde.fr/2012/01/08/17-est-le-nombre-de-dieu-au-sudoku/

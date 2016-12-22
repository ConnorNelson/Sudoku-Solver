# Sudoku-Solver
Solves [Sudoku](https://en.wikipedia.org/wiki/Sudoku) by reducing Sudoku to the [exact cover](https://en.wikipedia.org/wiki/Exact_cover) problem and using [Knuth's Algorithm X](https://en.wikipedia.org/wiki/Knuth's_Algorithm_X). The algorithm is implemented in Python 2.7 using the efficient [dancing links](https://en.wikipedia.org/wiki/Dancing_Links) technique.

# Usage
Redirect standard input:
```shell
python solver.py < [PATH TO PUZZLE]
```

## Input Sudoku Format
Columns are not separated, rows are separated by new lines 
Unknown values are represented by 0s 

Example: 
000790050 
352008040 
000000080 
010070004 
600301008 
900080010 
020000000 
040500891 
080037000 


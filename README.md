# Sudoku Solver

#### Source: [CALCUDOKU](https://www.calcudoku.org/en)

---
#### Killer Solver:
```
sudoku/killer

python3 tocnf.py
[enter url]
minisat killer.cnf solution.txt
python3 final.py
```

---
#### Calcudoku Solver:
You must install the binary of [Berkeley abc](https://github.com/berkeley-abc/abc) under directory `sudoku/calcudoku`. Also, please make sure `calcudoku/abc` is included in `sudoku/.gitignore` to avoid failure pushing to GitHub.
```
sudoku/calcudoku

python3 begin.py
[enter url]
./abc
abc 01> read_eqn begin.eqn
abc 02> strash
abc 03> write_eqn middle.eqn
abc 03> ^C
python3 middle.py
minisat middle.cnf solution.txt
python3 end.py
```


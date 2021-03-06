# https://www.freecodecamp.org/news/how-to-play-and-win-sudoku-using-math-and-machine-learning-to-solve-every-sudoku-puzzle/


from timeit import timeit


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    # To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  # (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


def solve(grid): return search(parse_grid(grid))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])


def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e:
            return e
    return False


puzzle = '000001200100700045000430700090006300050807020006200090003019000970004006002500000'
hardPuzzle = '''
8 5 . |. . 2 |4 . . 
7 2 . |. . . |. . 9 
. . 4 |. . . |. . . 
------+------+------
. . . |1 . 7 |. . 2 
3 . 5 |. . . |9 . . 
. 4 . |. . . |. . . 
------+------+------
. . . |. 8 . |. 7 . 
. 1 7 |. . . |. . . 
. . . |. 3 6 |. 4 .'''

# 189 seconds for Norvig, 132 on 2016 MacBook Pro
longSolve = '''
. . . |. . 6 |. . . 
. 5 9 |. . . |. . 8 
2 . . |. . 8 |. . . 
------+------+------
. 4 5 |. . . |. . . 
. . 3 |. . . |. . . 
. . 6 |. . 3 |. 5 4 
------+------+------
. . . |3 2 5 |. . 6 
. . . |. . . |. . . 
. . . |. . . |. . . '''

reallyHardPuzzles = '''85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.
..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..
12..4......5.69.1...9...5.........7.7...52.9..3......2.9.6...5.4..9..8.1..3...9.4
...57..3.1......2.7...234......8...4..7..4...49....6.5.42...3.....7..9....18.....
7..1523........92....3.....1....47.8.......6............9...5.6.4.9.7...8....6.1.
1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3..
1...34.8....8..5....4.6..21.18......3..1.2..6......81.52..7.9....6..9....9.64...2
...92......68.3...19..7...623..4.1....1...7....8.3..297...8..91...5.72......64...
.6.5.4.3.1...9...8.........9...5...6.4.6.2.7.7...4...5.........4...8...1.5.2.3.4.
7.....4...2..7..8...3..8.799..5..3...6..2..9...1.97..6...3..9...3..4..6...9..1.35
....7..2.8.......6.1.2.5...9.54....8.........3....85.1...3.2.8.4.......9.7..6....'''.split('\n')

# print(solve(hardPuzzle))
print(''.join([v for v in solve(hardPuzzle).values()]))

# for p in reallyHardPuzzles:
#     print(timeit(lambda: solve(p), number=1))


# print('hard puzzle', timeit(lambda: solve(hardPuzzle), number=1))
# print('long puzzle', timeit(lambda: solve(longSolve), number=1))

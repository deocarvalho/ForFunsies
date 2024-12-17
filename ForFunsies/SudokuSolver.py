def print_board(board):
    for row in board:
        print(" ".join(str(num) for num in row))

def is_safe(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:  # Check row
            return False
        if board[x][col] == num:  # Check column
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:  # Check 3x3 box
                return False
    return True

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True  # Solved
    row, col = empty

    for num in range(1, 10):  # Numbers 1-9
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Backtrack

    return False

def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:  # 0 indicates an empty cell
                return (i, j)
    return None

# Puzzle example
sudoku_puzzle = [
    [5, 4, 0, 9, 0, 7, 0, 3, 0],
    [0, 0, 0, 3, 0, 1, 5, 6, 4],
    [2, 1, 0, 0, 0, 4, 8, 0, 0],
    [0, 0, 8, 0, 0, 5, 0, 2, 0],
    [0, 0, 2, 0, 7, 9, 3, 0, 5],
    [3, 0, 1, 2, 4, 0, 0, 0, 9],
    [9, 8, 0, 0, 0, 0, 6, 5, 0],
    [0, 0, 0, 5, 6, 3, 0, 7, 8],
    [0, 3, 5, 7, 9, 0, 0, 0, 2],
]

if solve_sudoku(sudoku_puzzle):
    print_board(sudoku_puzzle)
else:
    print("No solution exists.")
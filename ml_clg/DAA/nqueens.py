global N
N = 4


def print_solution(board):
    for i in range(N):
        for j in range(N):
            print(board[i][j], end=" ")
        print()


def is_safe(board, row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False

    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    for i, j in zip(range(row, N, 1),
                    range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True


def solve_nqueens(board, col):
    if col >= N:
        return True

    for i in range(N):

        if is_safe(board, i, col):

            board[i][col] = 1

            if solve_nqueens(board, col + 1):
                return True

            board[i][col] = 0

    return False


def solvenqueens():
    board = [[0, 0, 0, 0],
             [1, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]

    if not solve_nqueens(board, 1):
        print("Solution does not exist")
        return False

    print_solution(board)
    return True


solvenqueens()


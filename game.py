import numpy as np

def get_starting_position():
    # positive number = white, negative number = black
    board = np.zeros(24, dtype=np.int8)
    # white pieces
    board[0] = 2
    board[11] = 5
    board[16] = 3
    board[18] = 5

    # black pieces
    board[23] = -2
    board[12] = -5
    board[7] = -3
    board[5] = -5

    white_bar = 0
    black_bar = 0
    turn = 0  # 0 = white, 1 = black
    return (board, white_bar, black_bar, turn)


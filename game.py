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
    turn = 1  # 1 = white, -1 = black
    return (board, white_bar, black_bar, turn)


def generate_following_states_one_dice_black_turn(board, white_bar, black_bar, dice):

    # blacks home is at position -1 so the playing direction is decresing. The last position is 23
    # The dice is a number between 1 and 6
    
    # first we check if there is a piece in the bar, that needs to be played
    if black_bar > 0:
        # we need to check if the relative field is empty:
        # if the dice is a 1, we need to check position 23 etc
        if board[24-dice] > 1:
            # the position is blocked so there is no valid move
            return []
        
        elif board[24-dice] == 1:
            # there is only a single white piece on the position, so this piece gets send to the bar
            next_board = board.copy()
            next_board[24-dice] = -1
            next_black_bar = black_bar - 1
            return [(next_board, white_bar + 1, next_black_bar)]    
        
        else:
            # the position is empty or already occupied by black so the move is valid and needs to be done
            # generate the following position
            next_board = board.copy()
            next_board[24-dice] -= 1
            next_black_bar = black_bar - 1
            return [(next_board, white_bar, next_black_bar)]
    
    # The bar is empty. Now we loop over all by black occupied positions and check if the move is possible
    # Here we only consider moves that do not save one of the black pieces in blacks goal.
    # we only need to start at the position dice.
    next_positions = []
    for i in range(dice, 24):
        if board[i] >= 0:
            # the position is not occupied by black so we continue with the next position
            continue
        # the position is occupied by black
        # we need to check if the position after dice jumps
        if board[i-dice] > 1: 
            # blocked by white
            continue 

        elif board[i-dice] == 1:
            # only one white piece on the fild, that gets send to the white bar
            next_board = board.copy()
            next_board[i] += 1
            next_board[i-dice] = -1
            next_positions.append((next_board, white_bar + 1, black_bar))

        else:
            # position is empty or already occupied by black
            next_board = board.copy()
            next_board[i] += 1
            next_board[i-dice] -= 1
            next_positions.append((next_board, white_bar, black_bar))


    # so we now need to consider all moves where one can safe a black piece in blacks basis

    # this is only allowed if all positions of blacks pieces are <= 5
    highest_black_position = None
    for i in range(23, -1, -1):
        if board[i] < 0:
            highest_black_position = i
            break
    
    if highest_black_position > 5:
        # not allowed to save black pieces in the base
        return next_positions
    
    # here it is allowed to save black pieces in the base.
    # dice 1 -> pos 0 can be saved
    # dice 2 -> pos 1 can be saved
    # -> if highest_black_position >= dice-1, then only the position dice-1 can be saved
    
    if board[dice-1] < 0:
        # there are black pieces on the position of the dice roll, so this checker needs to be beared off
        next_board = board.copy()
        next_board[dice-1] += 1
        next_positions.append((next_board, white_bar, black_bar))

    elif highest_black_position < dice - 1:
        # only possible way for bearing off is to bear off a checker at the highest_black_position
        next_board = board.copy()
        next_board[highest_black_position] += 1
        next_positions.append((next_board, white_bar, black_bar))

    return next_positions


if __name__ == "__main__":
    s = get_starting_position()

    following_positions = generate_following_states_one_dice_black_turn(s[0], s[1], s[2], 5)
    print(following_positions)
    print(len(following_positions))




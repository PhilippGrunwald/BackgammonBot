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



def process_white_human_move(board, white_bar, black_bar, dice, input):

    if input == "-":
        return (board, white_bar, black_bar)

    if input == "BAR":
        print("YYYY")
        if white_bar <= 0:
            print("BAR not possible, since Bar is empty")
            return False
        # bar move
        # check if the position at dice-1 is occupied
        if board[dice-1] < -1:
            return False
        elif board[dice-1] == -1:
            next_board = board.copy()
            next_board[dice-1] = 1
            return (next_board, white_bar - 1, black_bar + 1)
        else:
            next_board = board.copy()
            next_board[dice-1] += 1
            return (next_board, white_bar - 1, black_bar)
        
    if white_bar > 0:
        print("input has to be 'BAR'")
        return False


    input = int(input)
    index = input - 1

    if index >= 24 or index < 0:
        print("input invalid range")
        return None

    if board[index] <= 0:
        # move is not possible, since there are no white pieces at the starting position
        print("move not possible!")
        return None
    
    if index + dice <= 23:
        start = index
        end = index + dice
        # not a bearing off move
        if board[end] < -1:
            print("Invalid move, positions blocked")
            return False
        if board[end] == -1:
            next_board = board.copy()
            next_board[start] -= 1
            next_board[end] = 1
            return (next_board, white_bar, black_bar + 1)
        else:
            next_board = board.copy()
            next_board[start] -= 1
            next_board[end] += 1
            return (next_board, white_bar, black_bar)
        
    else:
        # bearing off move
        # TODO add all rules:
        next_board = board.copy()
        next_board[index] -= 1
        return (next_board, white_bar, black_bar)



def generate_following_states_one_dice_black_turn(board, white_bar, black_bar, dice, next_positions, seen):
    # next_positions is the return array

    # blacks home is at position -1 so the playing direction is decresing. The last position is 23
    # The dice is a number between 1 and 6
    
    # first we check if there is a piece in the bar, that needs to be played
    if black_bar > 0:
        # we need to check if the relative field is empty:
        # if the dice is a 1, we need to check position 23 etc
        if board[24-dice] > 1:
            # the position is blocked so there is no valid move
            return True
        
        elif board[24-dice] == 1:
            # there is only a single white piece on the position, so this piece gets send to the bar
            next_board = board.copy()
            next_board[24-dice] = -1
            key = (tuple(next_board, white_bar, black_bar)) 
            if key not in seen:
                next_positions.append((next_board, white_bar + 1, black_bar - 1))
                seen.add(key)
            return True    
        
        else:
            # the position is empty or already occupied by black so the move is valid and needs to be done
            # generate the following position
            next_board = board.copy()
            next_board[24-dice] -= 1
            key = (tuple(next_board), white_bar, black_bar - 1)
            if key not in seen:
                next_positions.append((next_board, white_bar, black_bar - 1))
                seen.add(key)
            return True
    
    # The bar is empty. Now we loop over all by black occupied positions and check if the move is possible
    # Here we only consider moves that do not save one of the black pieces in blacks goal.
    # we only need to start at the position dice.
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
            key = (tuple(next_board), white_bar + 1, black_bar)
            if key not in seen:
                next_positions.append((next_board, white_bar + 1, black_bar))
                seen.add(key)

        else:
            # position is empty or already occupied by black
            next_board = board.copy()
            next_board[i] += 1
            next_board[i-dice] -= 1
            key = (tuple(next_board), white_bar, black_bar)
            if key not in seen:
                next_positions.append((next_board, white_bar, black_bar))
                seen.add(key)

    # so we now need to consider all moves where one can safe a black piece in blacks basis

    # this is only allowed if all positions of blacks pieces are <= 5
    highest_black_position = None
    for i in range(23, -1, -1):
        if board[i] < 0:
            highest_black_position = i
            break
    
    if highest_black_position > 5:
        # not allowed to save black pieces in the base
        return True
    
    # here it is allowed to save black pieces in the base.
    # dice 1 -> pos 0 can be saved
    # dice 2 -> pos 1 can be saved
    # -> if highest_black_position >= dice-1, then only the position dice-1 can be saved
    
    if board[dice-1] < 0:
        # there are black pieces on the position of the dice roll, so this checker needs to be beared off
        next_board = board.copy()
        next_board[dice-1] += 1
        key = (tuple(next_board), white_bar, black_bar)
        if key not in seen:
            next_positions.append((next_board, white_bar, black_bar))
            seen.add(key)

    elif highest_black_position < dice - 1:
        # only possible way for bearing off is to bear off a checker at the highest_black_position
        next_board = board.copy()
        next_board[highest_black_position] += 1
        key = (tuple(next_board), white_bar, black_bar)
        if key not in seen:
            seen.add(key)
            next_positions.append((next_board, white_bar, black_bar))

    return True



def generate_following_states_one_dice_white_turn(board, white_bar, black_bar, dice, next_positions, seen):

    # whites home is at position 24 so the playing direction is increasing. The last position is 0
    # The dice is a number between 1 and 6
    
    # first we check if there is a piece in the bar, that needs to be played
    if white_bar > 0:
        # we need to check if the relative field is empty:
        # if the dice is a 1, we need to check position 23 etc
        if board[dice-1] < -1:
            # the position is blocked so there is no valid move
            return True
        
        elif board[dice-1] == -1:
            # there is only a single black piece on the position, so this piece gets send to the bar
            next_board = board.copy()
            next_board[dice-1] = 1
            key = (tuple(next_board), white_bar - 1, black_bar + 1)
            if key not in seen:
                seen.add(key)
                next_positions.append((next_board, white_bar - 1, black_bar + 1))
            return True   
        
        else:
            # the position is empty or already occupied by white so the move is valid and needs to be done
            # generate the following position
            next_board = board.copy()
            next_board[dice-1] += 1
            key = (tuple(next_board), white_bar - 1, black_bar)
            if key not in seen:
                seen.add(key)
                next_positions.append((next_board, white_bar - 1, black_bar))
            return True

    # The bar is empty. Now we loop over all by white occupied positions and check if the move is possible
    # Here we only consider moves that do not save one of the white pieces in whites goal.
    # we only need to check to the 23-dice position.
    for i in range(0, 23 - dice):
        if board[i] <= 0:
            # the position is not occupied by black so we continue with the next position
            continue
        # the position is occupied by black
        # we need to check if the position after dice jumps
        if board[i+dice] < -1: 
            # blocked by white
            continue 

        elif board[i+dice] == -1:
            # only one black piece on the field, that gets send to the black bar
            next_board = board.copy()
            next_board[i] -= 1
            next_board[i+dice] = 1
            key = (tuple(next_board), white_bar, black_bar + 1)
            if key not in seen:
                seen.add(key)
                next_positions.append((next_board, white_bar, black_bar + 1))

        else:
            # position is empty or already occupied by white
            next_board = board.copy()
            next_board[i] -= 1
            next_board[i+dice] += 1
            key = (tuple(next_board), white_bar, black_bar)
            if key not in seen:
                seen.add(key)
                next_positions.append((next_board, white_bar, black_bar))


    # so we now need to consider all moves where one can safe a black piece in blacks basis

    # this is only allowed if all positions of blacks pieces are <= 5
    lowest_white_position = None
    for i in range(0, 24, 1):
        if board[i] > 0:
            lowest_white_position = i
            break
    
    if lowest_white_position <= 17:
        # not allowed to save black pieces in the base
        return True
    
    # here it is allowed to save black pieces in the base.
    # dice 1 -> pos 0 can be saved
    # dice 2 -> pos 1 can be saved
    # -> if highest_black_position >= dice-1, then only the position dice-1 can be saved
    
    if board[24-dice] > 0:
        # there are white pieces on the position of the dice roll, so this checker needs to be beared off
        next_board = board.copy()
        next_board[24-dice] -= 1
        key = (tuple(next_board), white_bar, black_bar)
        if key not in seen:
            seen.add(key)
            next_positions.append((next_board, white_bar, black_bar))

    elif lowest_white_position > 24 - dice:
        # only possible way for bearing off is to bear off a checker at the highest_black_position
        next_board = board.copy()
        next_board[lowest_white_position] -= 1
        key = (tuple(next_board), white_bar, black_bar)
        if key not in seen:
            seen.add(key)

            next_positions.append((next_board, white_bar, black_bar))

    return True



def generate_following_states_black(board, white_bar, black_bar, dice1, dice2):
    seen = set()
    if dice1 == dice2:
        d1 = []
        d2 = []
        d3 = []
        d4 = []
        generate_following_states_one_dice_black_turn(board, white_bar, black_bar, dice1, d1, seen)
        for position in d1:
            generate_following_states_one_dice_black_turn(position[0], position[1], position[2], dice1, d2, seen)
        seen = set()
        for position in d2:
            generate_following_states_one_dice_black_turn(position[0], position[1], position[2], dice1, d3, seen)
        seen = set()
        for position in d3:
            generate_following_states_one_dice_black_turn(position[0], position[1], position[2], dice1, d4, seen)
        return d4        


    after_dice1 = []
    after_dice2 = []
    seen = set()
    generate_following_states_one_dice_black_turn(board, white_bar, black_bar, dice1, after_dice1, seen)
    seen = set()
    generate_following_states_one_dice_black_turn(board, white_bar, black_bar, dice2, after_dice2, seen)
    
    seen = set()
    next_positions = []
    for position in after_dice1:
        generate_following_states_one_dice_black_turn(position[0], position[1], position[2], dice2, next_positions, seen)
    for position in after_dice2:
        generate_following_states_one_dice_black_turn(position[0], position[1], position[2], dice1, next_positions, seen)
    
    return next_positions
    


def generate_following_states_white(board, white_bar, black_bar, dice1, dice2):
    seen = set()
    if dice1 == dice2:
        d1 = []
        d2 = []
        d3 = []
        d4 = []
        generate_following_states_one_dice_white_turn(board, white_bar, black_bar, dice1, d1, seen)
        seen = set()
        for position in d1:
            generate_following_states_one_dice_white_turn(position[0], position[1], position[2], dice1, d2, seen)
        seen = set()
        for position in d2:
            generate_following_states_one_dice_white_turn(position[0], position[1], position[2], dice1, d3, seen)
        seen = set()
        for position in d3:
            generate_following_states_one_dice_white_turn(position[0], position[1], position[2], dice1, d4, seen)
        return d4        


    after_dice1 = []
    after_dice2 = []
    seen = set()
    generate_following_states_one_dice_white_turn(board, white_bar, black_bar, dice1, after_dice1, seen)
    seen = set()
    generate_following_states_one_dice_white_turn(board, white_bar, black_bar, dice2, after_dice2, seen)
    seen = set()
    next_positions = []
    for position in after_dice1:
        generate_following_states_one_dice_white_turn(position[0], position[1], position[2], dice2, next_positions, seen)
    for position in after_dice2:
        generate_following_states_one_dice_white_turn(position[0], position[1], position[2], dice1, next_positions, seen)
    
    return next_positions
  


def evaluate(board, white_bar, black_bar):
    # score will be high if the position is in favor of black and low otherwise
    score = 0
    score += 60 * white_bar
    score -= 80 * black_bar

    #  get the highest black piece
    highest_black_position = None
    for i in range(23, -1, -1):
        if board[i] < 0:
            highest_black_position = i
            break
    
    lowest_white_position = None
    for i in range(0, 24, 1):
        if board[i] > 0:
            lowest_white_position = i
            break

    for i, position in enumerate(board):

        # white home at position 24, black home at position 0
        if position > 0:
            # white occupied
            score += (24 - i) * 1.5 * abs(position)
        elif position < 0:
            # black occupied
            score -= i * 3 * abs(position)

        if position == 1 and highest_black_position > i:
            # single white checker -> good!
            score += i * 5
        
        if position == -1 and lowest_white_position < i:
            # bad!
            score -= (24-i) * 7

    return score



def simple_next_black_move(board, white_bar, black_bar, dice1, dice2):

    possible_moves = generate_following_states_black(board, white_bar, black_bar, dice1, dice2)

    max_expected = -100000000000000000000000
    best_state = (board, white_bar, black_bar)
    for state in possible_moves:

        # generate all possible dice combinations
        # start an expectimax
        expected_value = 0
        for i in range(1, 7):
            for j in range(i, 6):
                possible_moves_white = generate_following_states_white(state[0], state[1], state[2], i, j)
                evaluations = [evaluate(p_move[0], p_move[1], p_move[2]) for p_move in possible_moves_white]
                if len(evaluations) > 0:
                    min_eval = min(evaluations)
                else:
                    min_eval = -100
                expected_value += 1 / 36 * min_eval if i == j else 1 / 18 * min_eval

        if expected_value >= max_expected:
            max_expected = expected_value
            best_state = state

    return best_state  




if __name__ == "__main__":
    s = get_starting_position()
    next = simple_next_black_move(s[0], s[1], s[2], 4, 4)
    # following_positions = generate_following_states_one_dice_white_turn(s[0], 0, 0, 5, return_array)
    print(next)



"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count for X O in board 
    x = 0
    o = 0
    for row in board:
        for element in row:
            if element == 'X':
                x += 1
            elif element == 'O':
                o += 1

    # Since X go 1st if X>O then O turn else X turn
    if x > o:
        return 'O'
    
    else:
        return 'X'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Return All EMPTY element
    actions_set = set()
    # Loop through every element in i th row and j th column
    for i in range(3):
        for j in range(3):
            # Check if empty
            if board[i][j] == EMPTY:
                actions_set.add((i,j))
    
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check invalid action
    i = action[0]
    j = action[1]
    if board[i][j] is not EMPTY:
        raise "Invalid Action"
    
    # Make Deep copy and use player(board) to define 'X' 'O'
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
   
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for X row win situation
    if board[0][0] == 'X' and board[0][1] == 'X' and board[0][2] == 'X':
        return 'X'
    elif board[1][0] == 'X' and board[1][1] == 'X' and board[1][2] == 'X':
        return 'X'
    elif board[2][0] == 'X' and board[2][1] == 'X' and board[2][2] == 'X':
        return 'X'

    # Check for X column win situation
    elif board[0][0] == 'X' and board[1][0] == 'X' and board[2][0] == 'X':
        return 'X'
    elif board[0][1] == 'X' and board[1][1] == 'X' and board[2][1] == 'X':
        return 'X'
    elif board[0][2] == 'X' and board[1][2] == 'X' and board[2][2] == 'X':
        return 'X'

    # Check for X diagonal win situation
    elif board[0][0] == 'X' and board[1][1] == 'X' and board[2][2] == 'X':
        return 'X'
    elif board[0][2] == 'X' and board[1][1] == 'X' and board[2][0] == 'X':
        return 'X'

    # Check for O row win situation
    if board[0][0] == 'O' and board[0][1] == 'O' and board[0][2] == 'O':
        return 'O'
    elif board[1][0] == 'O' and board[1][1] == 'O' and board[1][2] == 'O':
        return 'O'
    elif board[2][0] == 'O' and board[2][1] == 'O' and board[2][2] == 'O':
        return 'O'

    # Check for O column win situation
    elif board[0][0] == 'O' and board[1][0] == 'O' and board[2][0] == 'O':
        return 'O'
    elif board[0][1] == 'O' and board[1][1] == 'O' and board[2][1] == 'O':
        return 'O'
    elif board[0][2] == 'O' and board[1][2] == 'O' and board[2][2] == 'O':
        return 'O'

    # Check for O diagonal win situation
    elif board[0][0] == 'O' and board[1][1] == 'O' and board[2][2] == 'O':
        return 'O'
    elif board[0][2] == 'O' and board[1][1] == 'O' and board[2][0] == 'O':
        return 'O'

    # If no win return none
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Is there a winner?
    if winner(board):
        return True
    # Are there still empty space?
    elif len(actions(board)) == 0:
        return True
    # Game not over yet
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    

def max_value(board):
    # Is game over?
    if terminal(board):
        return utility(board)
    
    # Initial value
    v = -math.inf
    # Loop for every action
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    # Is game over?
    if terminal(board):
        return utility(board)
    
    # Initial value
    v = math.inf
    # Loop for every action
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Consider is ai is X or O for right utility values
    ai = player(board)
    # AI is Max Player
    if ai == X:
        max_action = max_value(board)
        for action in actions(board):
            if max_action == min_value(result(board, action)):
                return action

    # AI is Min Player
    else:
        min_action = min_value(board)
        for action in actions(board):
            if min_action == max_value(result(board, action)):
                return action
        
          
    
        

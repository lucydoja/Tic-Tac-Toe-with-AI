"""
Tic Tac Toe Player
"""

import math
import copy

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

    # If the board is on the initial state the move is for X
    if board == initial_state():
        return X
    else:
        # Else we count how many move have been made
        moves_counter = 0
        # Loop though the board matrix
        for i in range(3):
            for j in range(3):
                # We update the counter if the value is not empty
                if board[i][j] != EMPTY:
                    moves_counter += 1
        # Since X is the first to move if the number of moves is odd is O's turn
        if moves_counter % 2 == 1:
            return O
        # If the number is odd is X turn
        else:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # If the board is already finished/complete no moves can be made
    if terminal(board):
        return 0

    # Else return the possible moves as a set
    available_spaces = set()

    # Loop though the board matrix
    for i in range(3):
        for j in range(3):
            # If the space is empty we add it to set
            if board[i][j] == EMPTY:
                available_spaces.add((i, j))

    return available_spaces


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action can be made, else rase an error
    if action not in actions(board):
        raise Exception("This move can't be made")

    # Make a copy of the board to not modify the original one
    copied_board = copy.deepcopy(board)
    # Assing value according to player move
    # Modify board according to action provided
    copied_board[action[0]][action[1]] = player(board)

    return copied_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Matrix of winner moves
    possible_wins = [
        [[0,0], [0,1], [0,2]],
        [[1,0], [1,1], [1,2]],
        [[2,0], [2,1], [2,2]],
        [[0,0], [1,0], [2,0]],
        [[0,1], [1,1], [2,1]],
        [[0,2], [1,2], [2,2]],
        [[0,0], [1,1], [2,2]],
        [[0,2], [1,1], [2,0]]
    ]

    # Loop through the winner moves to check if there is a winner
    for win in possible_wins:
        # If a winning move is made return the winner
        if board[win[0][0]][win[0][1]] == board[win[1][0]][win[1][1]]  == board[win[2][0]][win[2][1]]:
            return board[win[0][0]][win[0][1]]
    # Else return no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If no winner or still available moves the game is not over
    if winner(board) != None:
        return True
    elif any(EMPTY in rows for rows in board):
        return False
    else:
        return True


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


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the game is terminal it should return none
    if terminal(board):
        return None

    # Return the best move
    if player(board) == X:
        # X tries to get the maximum value (1)
        value, move = max_value_and_move(board)
        return move
    else:
        # 0 tries to get the minimum value (0)
        value, move = min_value_and_move(board)
        return move


def max_value_and_move(board):
    """
    Returns the move that generates the maximum value
    """
    # Check if terminal
    if terminal(board):
        return utility(board), None

    # Declare minimum value possible
    value = float("-inf")
    move = None

    # Loop through the possible actions and find the one that returns the maximun value
    for action in actions(board):
        # Evaluate next player move
        result_value, result_move = min_value_and_move(result(board, action))
        # Check if the move is optimal
        if result_value > value:
            value = result_value
            move = action
            # If value gets maximun result stop loop and return value and move
            if value == 1:
                return value, move

    return value, move


def min_value_and_move(board):
    """
    Returns the move that generates the minimum value
    """
    # Check if terminal
    if terminal(board):
        return utility(board), None

    # Declare maximum value possible
    value = float("inf")
    move = None

    # Loop through the possible actions and find the one that returns the minimum value
    for action in actions(board):
        # Evaluate next player move
        result_value, result_move = max_value_and_move(result(board, action))
        # Check if the move is optimal
        if result_value < value:
            value = result_value
            move = action
            # If value gets minimum result stop loop and return value and move
            if value == -1:
                return value, move

    return value, move

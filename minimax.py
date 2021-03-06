from math import inf
from random import choice
from copy import deepcopy
from boardclasses import TicTacToeBoard


"""
This is a modified version of the minimax algorithm for Tic Tac Toe from the following source:
Link: https://github.com/Cledersonbc/tic-tac-toe-minimax

An implementation of Minimax AI Algorithm in Tic Tac Toe, using Python.
This software is available under GPL license.
Author: Clederson Cruz
Year: 2017
License: GNU GENERAL PUBLIC LICENSE (GPL)
"""


def heuristic(state, depth):
    """
    Heuristic evaluation of the current board state
    :param state: the current board state
    :param depth: the number of empty spaces left on the board. Preference is given for faster wins and slower losses.
    """
    if state.has_tic_tac_toe(COMP):
        score = depth + 1
    elif state.has_tic_tac_toe(HUMAN):
        score = -(depth + 1)
    else:  # draw/undetermined outcome
        score = 0
    return score


def get_empty_cells(state):
    """
    Returns the coordinates of all the unclaimed spaces on the board
    :param state: the current board state
    :return: The coordinates of all the empty cells left on the board
    """
    cells = []
    for row_index, row in enumerate(state.board):
        for col_index, cell in enumerate(row):
            if cell == 0:
                cells.append([row_index, col_index])
    return cells


def minimax(state, depth, player):
    """
    The minimax algorithm itself. Returns a random move if the depth is 9, otherwise the first move would always be the
    top left corner.
    :param state: the current board state
    :param depth: the number of empty spaces left on the board
    :param player: who makes the next move (1 or 2)
    :return: coordinates of the best move for the current branch at the current depth, along with the score of that
    move, defined by the heuristic function
    """
    if depth == 9:
        row = choice([0, 1, 2])
        col = choice([0, 1, 2])
        return row, col, ''

    if player == COMP:
        best = [-1, -1, float("-inf")]
    else:
        best = [-1, -1, float("inf")]

    if depth == 0 or state.has_tic_tac_toe(COMP) or state.has_tic_tac_toe(HUMAN):
        score = heuristic(state, depth)
        return [-1, -1, score]
    """
    Checks if any of the player is one away from winning in any board and make the appropriate move.
    """
    if player==COMP:
        empty_cells=get_empty_cells(state)
        dangerous_cells=state.is_one_away_from_tic_tac_toe((player%2)+1)
        if dangerous_cells:
            found_dangerous_cells=True
        else:
            found_dangerous_cells=False
            print "no dangerous local boards"
        favoring_cells=state.is_one_away_from_tic_tac_toe(player)
        if favoring_cells:
            found_favoring_cells=True
        else:
            found_favoring_cells=False
            print "no favoring local boards"
        if found_dangerous_cells==False and found_favoring_cells==False:
            pass
        if found_dangerous_cells==False and found_favoring_cells==True:
            empty_cells[:]=[]
            for cell in favoring_cells:
                empty_cells.append(cell)
        if found_dangerous_cells==True and found_favoring_cells==False:
            empty_cells[:]=[]
            for cell in dangerous_cells:
                empty_cells.append(cell)
        if found_dangerous_cells==True and found_favoring_cells==True:
            empty_cells[:]=[]
            for cell in dangerous_cells:
                empty_cells.append(cell)
    else:
        empty_cells=get_empty_cells(state)
    for cell in empty_cells:
        row, col = cell[0], cell[1]
        state.board[row][col] = player
        score = minimax(state, depth - 1, (player % 2) + 1)
        state.board[row][col] = 0
        score[0], score[1] = row, col
        if player == COMP:
            if score[2] >= best[2]:
                if score[2]==best[2]:
                    """
                    Favors middle positions over sides or corners
                    MIDDLE > CORNERS > SIDES
                    """
                    if (best[0]==0 and best[1]==0) or (best[0]==0 and best[1]==2) or (best[0]==2 and best[1]==0) or (best[0]==2 and best[1]==2):
                        if score[0]==0 and score[1]==0: #favoring centre position over diagonal position
                            best=score
                            print("centre position chosen over diagonal positions")
                    else:
                        if ((score[0]==0 and score[1]==1) or (score[0]==1 and score[1]==0) or (score[0]==1 and score[1]==2) or (score[0]==2 and score[1]==1))==0:
                            best=score  #favoring any position over side position as long as the new position is not a side position too
                            print("diagonal and centre positions chosen over side positions")
                else:
                    best = score
        else:
            bestMoves=[]
            if score[2] < best[2]:
                best=score
    return best


def bot_turn(global_board, bot):
    """
    Finds the next local board to play on. If undefined, it uses the minimax algorithm to decide which board to play on.
    Then uses the minimax algorithm again to decide where to play on that board.
    :param global_board: The entire global board of the game
    :param bot: is the bot player 1 or 2?
    :return: local_board and coordinates of the bot's next move
    """
    # Determine if the bot is player 1 or 2
    global COMP
    global HUMAN
    COMP = bot
    HUMAN = (bot % 2) + 1

    # If the next board is undetermined
    if all(lb.focus == lb.playable for lb in global_board.local_boards):
        # Use minimax on the global board to determine the next local board
        depth = len(get_empty_cells(global_board))
        state = TicTacToeBoard()
        state.board = deepcopy(global_board.board)
        row, col, _ = minimax(state, depth, COMP)
        local_board = global_board.local_boards[row * 3 + col]
    else:
        # Find the local board in focus
        for lb in global_board.local_boards:
            if lb.focus:
                local_board = lb
                break

    # local_board now defined. Now use minimax to find row and col of next move
    depth = len(get_empty_cells(local_board))
    state = TicTacToeBoard()
    state.board = deepcopy(local_board.board)
    row, col, _ = minimax(state, depth, COMP)

    return local_board, row, col

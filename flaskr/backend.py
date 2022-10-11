from pprint import pp, pprint
import numpy as np

X = 0
R = 1
Y = 2

board = [
    [0,0,0,Y,0,0,0],
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,Y,0,Y,0,0,0]
]

board_1 = [
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,R,0,R,0,0,0],
    [0,0,R,Y,0,0,0],
    [0,0,0,R,0,0,0],
    [Y,Y,Y,R,R,0,0]
]

def check_win(board):
    horizontal_base = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]
    vertical_base = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]
    diag_base = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]


    # horizontal
    for x in range(len(board[0])):
        for y in range(len(board)):
            if board[y][x] > 0:
                if x == 0:
                    if board[y][0] > 0:
                        horizontal_base[y][x] = 1
                else:
                    if board[y][x] == board[y][x-1]:
                        horizontal_base[y][x] = horizontal_base[y][x-1] + 1
                    else:
                        horizontal_base[y][x] = 1

    # vertical
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] > 0:
                if y == 0:
                    if board[0][x] > 0:
                        vertical_base[y][x] = 1
                else:
                    if board[y][x] == board[y-1][x]:
                        vertical_base[y][x] = vertical_base[y-1][x] + 1
                    else:
                        vertical_base[y][x] = 1
    
    # diag
    for x in range(len(board[0])):
        for y in range(len(board)):
            if board[y][x] > 0:
                if x == 0 or y == 0:
                    if board[y][x] > 0:
                        diag_base[y][x] = 1
                else:
                    if board[y][x] == board[y-1][x-1]:
                        diag_base[y][x] = diag_base[y-1][x-1] + 1
                    else:
                        diag_base[y][x] = 1
    print('horizontal')
    pprint(horizontal_base)
    print('vertical')
    pprint(vertical_base)
    print('diag')
    pprint(diag_base)

    winner = -1
    horizontal_base = np.array(horizontal_base)
    vertical_base = np.array(vertical_base)
    diag_base = np.array(diag_base)
    if np.amax(horizontal_base) >= 4:
        coords = np.unravel_index(horizontal_base.argmax(), horizontal_base.shape)
        winner = board[coords[0]][coords[1]]
    elif np.amax(vertical_base) >= 4:
        coords = np.unravel_index(vertical_base.argmax(), vertical_base.shape)
        winner = board[coords[0]][coords[1]]
    elif np.amax(diag_base) >= 4:
        coords = np.unravel_index(diag_base.argmax(), diag_base.shape)
        winner = board[coords[0]][coords[1]]
    return winner

def find_lowest_row(col,board):
    lowest_row = -1
    for row in range(len(board)):
        if board[row][col] == 0:
            lowest_row = row
    return lowest_row


def insert_counter(col, color):
    row = find_lowest_row(col, board)
    if row > -1:
        board[row][col] = color
    return board


def main():
    current_player = R
    
    # make turn
    # send board
    check_win

print(check_win(board_1))
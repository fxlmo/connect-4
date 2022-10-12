from pprint import pp, pprint
import random
import numpy as np
from requests import check_compatibility

X       = 0
R       = 1
Y       = 2
DRAW    = 3

# test boards

board_1 = [
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,Y,0,R,0,Y,0],
    [0,0,R,Y,Y,0,0],
    [0,0,0,Y,0,0,0],
    [Y,Y,Y,R,R,0,0]
]

board_2 = [
    [0,0,0,Y,0,0,0],
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,0,0,R,0,0,0],
    [0,Y,0,Y,0,0,0]
]

class game:
    def __init__(self) -> None:
        self.curr_player = random.randint(1,2)
        self.board       = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ]
        self.in_progress = True
    
    def reset_game(self):
        self.curr_player = random.randint(1,2)
        self.board       = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ]
        self.in_progress = True

    def check_win(self):
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
        diag_base_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ]


        # horizontal
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] > 0:
                    if x == 0:
                        if self.board[y][0] > 0:
                            horizontal_base[y][x] = 1
                    else:
                        if self.board[y][x] == self.board[y][x-1]:
                            horizontal_base[y][x] = horizontal_base[y][x-1] + 1
                        else:
                            horizontal_base[y][x] = 1

        # vertical
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                if self.board[y][x] > 0:
                    if y == 0:
                        if self.board[0][x] > 0:
                            vertical_base[y][x] = 1
                    else:
                        if self.board[y][x] == self.board[y-1][x]:
                            vertical_base[y][x] = vertical_base[y-1][x] + 1
                        else:
                            vertical_base[y][x] = 1
        
        # diag
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[y][x] > 0:
                    if x == 0 or y == 0:
                        if self.board[y][x] > 0:
                            diag_base[y][x] = 1
                    else:
                        if self.board[y][x] == self.board[y-1][x-1]:
                            diag_base[y][x] = diag_base[y-1][x-1] + 1
                        else:
                            diag_base[y][x] = 1

        # diag_1
        for x in reversed(range(len(self.board[0]))):
            for y in range(len(self.board)):
                if self.board[y][x] > 0:
                    if x == 6 or y == 0:
                        if self.board[y][x] > 0:
                            diag_base_1[y][x] = 1
                    else:
                        if self.board[y][x] == self.board[y-1][x+1]:
                            diag_base_1[y][x] = diag_base_1[y-1][x+1] + 1
                        else:
                            diag_base_1[y][x] = 1
        # print('horizontal')
        # pprint(horizontal_base)
        # print('vertical')
        # pprint(vertical_base)
        # print('diag')
        # pprint(diag_base)
        # print('diag_1')
        # pprint(diag_base_1)

        winner = -1
        horizontal_base = np.array(horizontal_base)
        vertical_base = np.array(vertical_base)
        diag_base = np.array(diag_base)
        diag_base_1 = np.array(diag_base_1)
        if np.amax(horizontal_base) >= 4:
            coords = np.unravel_index(horizontal_base.argmax(), horizontal_base.shape)
            winner = self.board[coords[0]][coords[1]]
        elif np.amax(vertical_base) >= 4:
            coords = np.unravel_index(vertical_base.argmax(), vertical_base.shape)
            winner = self.board[coords[0]][coords[1]]
        elif np.amax(diag_base) >= 4:
            coords = np.unravel_index(diag_base.argmax(), diag_base.shape)
            winner = self.board[coords[0]][coords[1]]
        elif np.amax(diag_base_1) >= 4:
            coords = np.unravel_index(diag_base_1.argmax(), diag_base.shape)
            winner = self.board[coords[0]][coords[1]]
        draw = True
        if winner == -1:
            for c in self.check_col_full():
                if not c:
                    draw = False
        else:
            draw = False
        if draw:
            winner = DRAW
        return winner

    def find_lowest_row(self, col):
        lowest_row = -1
        for row in range(len(self.board)):
            if self.board[row][col] == 0:
                lowest_row = row
        return lowest_row


    def insert_counter(self,col, color):
        row = self.find_lowest_row(col)
        if row > -1:
            self.board[row][col] = color
        return self.board

    def check_col_full(self):
        top_col = self.board[0]
        full_list = []
        for c in top_col:
            if c > 0:
                full_list.append(True)
            else:
                full_list.append(False)
        return full_list
    
    def make_move(self, col):
        full_col = self.check_col_full()
        if not (full_col[col]):
            self.insert_counter(col, self.curr_player)
            gamestate = self.check_win()
            if self.curr_player == Y: self.curr_player = R
            else: self.curr_player = Y
            if gamestate == -1:
                # in progress
                pass
            else:
                self.in_progress = False
            return (gamestate)
        else:
            return -1



def main():
    current_player = R
    
    # make turn
    # send board
    # check_win

# print(check_win(board_1))
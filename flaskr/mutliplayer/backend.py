from distutils.command.check import check
import math
from pprint import pp, pprint
import random
import numpy as np
from requests import check_compatibility

X       = 0
R       = 1
Y       = 2
DRAW    = 3
WINDOW_LENGTH   = 4
ROW_COUNT       = 6
COLUMN_COUNT    = 7

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
    def __init__(self, ai=False) -> None:
        self.curr_player = R
        self.board       = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ]
        self.ai = ai
        if self.curr_player == Y:
            self.ai_colour = R
            self.player_colour = Y
        else:
            self.ai_colour = Y
            self.player_colour = R
        self.in_progress = True
    
    def reset_game(self, ai=False):
        self.curr_player = R
        self.board       = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ]
        self.ai = ai
        if self.curr_player == Y:
            self.ai_colour = R
            self.player_colour = Y
        else:
            self.ai_colour = Y
            self.player_colour = R
        self.in_progress = True

    def board_to_ascii(self, b):
        board = []
        for col in b:
            board.append([" " if c == X else "X" if c == R else "O" for c in col])
        for col in board:
            for cell in col:
                if cell == X:
                    cell = " "
                elif cell == R:
                    cell = "X"
                elif cell == Y:
                    cell = "O"
        print(board)
        output  = f"╔═══╦═══╦═══╦═══╦═══╦═══╦═══╗\n"
        output += f"║ {board[0][0]} ║ {board[0][1]} ║ {board[0][2]} ║ {board[0][3]} ║ {board[0][4]} ║ {board[0][5]} ║ {board[0][6]} ║\n"
        output += f"╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣\n"
        output += f"║ {board[1][0]} ║ {board[1][1]} ║ {board[1][2]} ║ {board[1][3]} ║ {board[1][4]} ║ {board[1][5]} ║ {board[1][6]} ║ \n"
        output += f"╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣\n"
        output += f"║ {board[2][0]} ║ {board[2][1]} ║ {board[2][2]} ║ {board[2][3]} ║ {board[2][4]} ║ {board[2][5]} ║ {board[2][6]} ║ \n"
        output += f"╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣\n"
        output += f"║ {board[3][0]} ║ {board[3][1]} ║ {board[3][2]} ║ {board[3][3]} ║ {board[3][4]} ║ {board[3][5]} ║ {board[3][6]} ║ \n"
        output += f"╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣\n"
        output += f"║ {board[4][0]} ║ {board[4][1]} ║ {board[4][2]} ║ {board[4][3]} ║ {board[4][4]} ║ {board[4][5]} ║ {board[4][6]} ║ \n"
        output += f"╠═══╬═══╬═══╬═══╬═══╬═══╬═══╣\n"
        output += f"║ {board[5][0]} ║ {board[5][1]} ║ {board[5][2]} ║ {board[5][3]} ║ {board[5][4]} ║ {board[5][5]} ║ {board[5][6]} ║ \n"
        output += f"╚═══╩═══╩═══╩═══╩═══╩═══╩═══╝\n"
        return output

    def check_win(self, board):
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

        # diag_1
        for x in reversed(range(len(board[0]))):
            for y in range(len(board)):
                if board[y][x] > 0:
                    if x == 6 or y == 0:
                        if board[y][x] > 0:
                            diag_base_1[y][x] = 1
                    else:
                        if board[y][x] == board[y-1][x+1]:
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
            winner = board[coords[0]][coords[1]]
        elif np.amax(vertical_base) >= 4:
            coords = np.unravel_index(vertical_base.argmax(), vertical_base.shape)
            winner = board[coords[0]][coords[1]]
        elif np.amax(diag_base) >= 4:
            coords = np.unravel_index(diag_base.argmax(), diag_base.shape)
            winner = board[coords[0]][coords[1]]
        elif np.amax(diag_base_1) >= 4:
            coords = np.unravel_index(diag_base_1.argmax(), diag_base.shape)
            winner = board[coords[0]][coords[1]]
        draw = True
        if winner == -1:
            for c in self.check_col_full(board):
                if not c:
                    draw = False
        else:
            draw = False
        if draw:
            winner = DRAW
        return winner

    def find_lowest_row(self, col, board):
        lowest_row = -1
        for row in range(len(board)):
            if board[row][col] == 0:
                lowest_row = row
        return lowest_row


    def insert_counter(self,col, color, board):
        new_board = board.copy()
        row = self.find_lowest_row(col, new_board)
        if row > -1:
            board[row][col] = color
        return new_board

    def check_col_full(self, board):
        top_col = board[0]
        full_list = []
        for c in top_col:
            if c > 0:
                full_list.append(True)
            else:
                full_list.append(False)
        return full_list
    
    def make_move(self, col, player, board):
        full_col = self.check_col_full(board)
        if not (full_col[col]):
            board = list(self.insert_counter(col, player, board))
            gamestate = self.check_win(board)
            if gamestate != -1:
                self.in_progress = False
            return (gamestate, board)
        else:
            return (-1, board)
    
    def update_player(self):
        if self.curr_player == Y: self.curr_player = R
        else: self.curr_player = Y
    
    # returns column
    def make_ai_move(self):
        # get list of valid moves for a board state
        def get_valid_moves(board):
            valid_moves = []
            col = 0
            for c in self.check_col_full(board):
                if not c:
                    valid_moves.append(col)
                col += 1
            return valid_moves


        # pick a random move from the possible moves
        def random_move():
            return random.choice(get_valid_moves(self.board))
        
        def minimax_move(board, ai_colour):
            valid_moves = get_valid_moves(self.board)
            scored_moves = {}
            
            new_board = list(map(list, board))
            for m in valid_moves:
                scored_moves[m] = minimax(new_board, 1, 4, ai_colour)
            best_move = max(scored_moves, key=scored_moves.get)
            print(scored_moves)
            return max(scored_moves, key = scored_moves.get)

        # maximise score for ai, minimise score for player
        def minimax(board, depth, alpha, beta, max_player):
            valid_moves = get_valid_moves(board)
            board_state = self.check_win(board)
            if board_state > 0 or depth == 0:
                if depth == 0:
                    return (None, score_position(board, self.ai_colour))
                elif board_state == DRAW:
                    return (None, 0)
                elif board_state == self.ai_colour:
                    return (None, 1000000000000000)
                elif board_state == self.player_colour:
                    return (None, -1000000000000000)
            if max_player:
                value = -math.inf
                column = random.choice(valid_moves)
                for col in valid_moves:
                    b_copy = list(map(list,board))
                    self.make_move(col, self.ai_colour, b_copy)
                    new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return column, value
            else:
                value = math.inf
                column = random.choice(valid_moves)
                for col in valid_moves:
                    b_copy = list(map(list,board))
                    self.make_move(col, self.player_colour, b_copy)
                    new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return column, value
        
        def score_position(board, colour):
            score = 0

            ## Score center column
            center_array = [i[COLUMN_COUNT//2] for i in board]
            center_count = center_array.count(colour)
            score += center_count * 3

            ## Score Horizontal
            for row_array in board:
                for c in range(COLUMN_COUNT-3):
                    window = row_array[c:c+WINDOW_LENGTH]
                    score += evaluate_window(window, colour)

            ## Score Vertical
            for c in range(COLUMN_COUNT):
                col_array = [i[c] for i in board]
                for r in range(ROW_COUNT-3):
                    window = col_array[r:r+WINDOW_LENGTH]
                    score += evaluate_window(window, colour)

            ## Score positive sloped diagonal
            for r in range(ROW_COUNT-3):
                for c in range(COLUMN_COUNT-3):
                    window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                    score += evaluate_window(window, colour)

            for r in range(ROW_COUNT-3):
                for c in range(COLUMN_COUNT-3):
                    window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                    score += evaluate_window(window, colour)

            return score

        def evaluate_window(window, piece):
            score = 0
            opp_piece = self.player_colour
            if piece == self.player_colour:
                opp_piece = self.ai_colour

            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(X) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(X) == 2:
                score += 2
            elif window.count(piece) == 2 and window.count(X) == 1:
                score += 1

            if window.count(opp_piece) == 3 and window.count(X) == 1:
                score -= 4

            return score

        # selected_move = random_move()
        selected_move = minimax(self.board, 5, -math.inf, math.inf, True)
        print(selected_move)
        return selected_move[0]



def main():
    current_player = R
    
    # make turn
    # send board
    # check_win

# print(check_win(board_1))
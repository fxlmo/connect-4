from backend import game

X       = 0
R       = 1
Y       = 2
DRAW    = 3

ROW_COUNT       = 6
COLUMN_COUNT    = 7

board_1 = [
    [Y,Y,Y,R,Y,Y,Y],
    [Y,Y,Y,R,Y,Y,Y],
    [Y,R,Y,R,Y,Y,Y],
    [Y,R,R,Y,Y,R,Y],
    [R,R,R,Y,R,R,Y],
    [Y,R,Y,R,R,R,Y]
]

game = game()

print(game.board_to_ascii(board_1))
from cmath import exp
import logging
from types import new_class

from backend import game

X = 0
Y = 1
R = 2
DRAW = 3

class TestMoves:
    @staticmethod
    def test_blank_at_start():
        new_game = game()
        blank_board = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ]

        assert new_game.board == blank_board

    @staticmethod
    def test_make_move_red():
        new_game = game()
        expected_board = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,R,0,0,0]
        ]

        new_game.make_move(3, R, new_game.board)

        assert new_game.board == expected_board

    @staticmethod
    def test_make_move_yellow():
        new_game = game()
        expected_board = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,Y,0,0,0]
        ]

        new_game.make_move(3, Y, new_game.board)

        assert new_game.board == expected_board

    @staticmethod
    def test_make_multiple_moves():
        new_game = game()
        expected_board = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,Y,0,0,0]
        ]

        new_game.make_move(3, Y, new_game.board)
        new_game.make_move(3, R, new_game.board)
        new_game.make_move(3, Y, new_game.board)

        assert new_game.board == expected_board

    @staticmethod
    def test_cant_move_on_full_col():
        new_game = game()
        expected_board = [
            [0,0,0,R,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,Y,0,0,0]
        ]

        new_game.board = expected_board
        new_game.make_move(3, Y, new_game.board)

        assert new_game.board == expected_board


class TestEndGame:
    @staticmethod
    def test_horizontal_win_red():
        board_1 = [
            [0,0,0,R,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,Y,0,0,0],
            [Y,R,R,R,R,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == R

    @staticmethod
    def test_horizontal_win_yellow():
        board_1 = [
            [0,0,0,R,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,Y,0,0,0],
            [Y,Y,Y,Y,R,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == Y

    @staticmethod
    def test_vertical_win_red():
        board_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,R,0,0,0],
            [0,0,0,R,0,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == R

    @staticmethod
    def test_vertical_win_yellow():
        board_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,Y,0,0,0],
            [0,0,0,Y,0,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == Y

    @staticmethod
    def test_diag_down_win_red():
        board_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [R,0,0,0,0,0,0],
            [0,R,0,0,0,0,0],
            [0,0,R,0,0,0,0],
            [0,0,0,R,0,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == R

    @staticmethod
    def test_diag_down_win_yellow():
        board_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [Y,0,0,0,0,0,0],
            [0,Y,0,0,0,0,0],
            [0,0,Y,0,0,0,0],
            [0,0,0,Y,0,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == Y

    @staticmethod
    def test_diag_up_win_red():
        board_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,R],
            [0,0,0,0,0,R,0],
            [0,0,0,0,R,0,0],
            [0,0,0,R,0,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == R

    @staticmethod
    def test_diag_up_win_yellow():
        board_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,Y],
            [0,0,0,0,0,Y,0],
            [0,0,0,0,Y,0,0],
            [0,0,0,Y,0,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == Y

    @staticmethod
    def test_draw():
        board_1 = [
            [R,Y,R,Y,R,Y,R],
            [R,Y,Y,R,R,Y,Y],
            [Y,R,Y,R,Y,R,Y],
            [R,Y,Y,R,R,R,Y],
            [R,R,R,Y,Y,Y,R],
            [Y,Y,R,Y,R,R,R]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == DRAW

    @staticmethod
    def test_in_progress():
        board_1 = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,Y,0,0,0]
        ]
        new_game = game()
        
        gamestate = new_game.check_win(board_1)
        assert gamestate == -1

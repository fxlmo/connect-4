import calendar
import datetime
import os
import pprint

from idna import check_bidi

import backend
from flask import Flask, make_response, render_template, request

from flaskr.backend import DRAW

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    game = backend.game()


    @app.route("/",methods = ["GET","POST"])
    def home():
        return render_template("homepage.html")

    @app.route("/game",methods = ["GET","POST"])
    def route():
        gamestate = -1
        col_full = game.check_col_full(game.board)
        if request.method == "POST":
            if request.form.get('new-game') != None:
                game.reset_game()
                col_full = game.check_col_full(game.board)
            elif request.form.get('column') != None:
                column_no = int(request.form.get('column'))
                (gamestate, game.board) = game.make_move(column_no, game.curr_player, game.board)
                if gamestate > 0:
                    col_full = [True, True, True, True, True, True, True]
                else:
                    col_full = game.check_col_full(game.board)
                game.update_player()
        return render_template("index.html", board=game.board, column_full=col_full,gamestate=gamestate)

    # 1 player game against ai
    @app.route("/ai-game",methods = ["GET","POST"])
    def ai_game():
        gamestate = -1
        col_full = game.check_col_full(game.board)
        if request.method == "POST":
            if request.form.get('new-game') != None:
                game.reset_game(ai=True)
                col_full = game.check_col_full(game.board)
            elif request.form.get('column') != None:
                column_no = int(request.form.get('column'))
                if game.curr_player == game.player_colour:
                    (gamestate, game.board) = game.make_move(column_no, game.curr_player, game.board)
                    game.update_player()
                    if gamestate == -1:
                        (gamestate, game.board) = game.make_move(game.make_ai_move(), game.ai_colour, game.board)
                        game.update_player()
                if gamestate > 0:
                    col_full = [True, True, True, True, True, True, True]
                else:
                    col_full = game.check_col_full(game.board)
        return render_template("ai-index.html", board=game.board, column_full=col_full,gamestate=gamestate)
    return app

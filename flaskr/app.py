import calendar
import datetime
import os
import pprint

from backend import game
from flask import Flask, make_response, render_template, request

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

    game = game()


    @app.route("/",methods = ["GET","POST"])
    def home():
        return render_template("homepage.html")

    @app.route("/game",methods = ["GET","POST"])
    def route():
        if request.method == "POST":
            if request.form.get('new-game') != None:
                game.reset_game()
            elif request.form.get('column') != None:
                column_no = int(request.form.get('column'))
                gamestate = game.make_move(column_no)
                #TODO: check gamestate

        return render_template("index.html", board=game.board, column_full=game.check_col_full)
    return app

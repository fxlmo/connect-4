import calendar
import datetime
import os
import pprint

#import backend
from flask import Flask, make_response, render_template, request

@app.route("/",methods = ["GET","POST"])
def route():
    if request.method == "POST":
        print(request.form.get("col"))
    return render_template("index.html")

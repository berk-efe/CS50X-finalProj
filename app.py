import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///keepTrack.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def games():
    return render_template('games.html')



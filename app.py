import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import get_deals

# Configure application
app = Flask(__name__)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///keepTrack.db")

@app.route('/')
def index():
    highlights = get_deals()
    
    context = {
        'highlights': highlights
    }
    
    return render_template('index.html', **context)

@app.route('/games')
def games():

    deals = get_deals(limit=15)
    
    context = {
        'deals': deals
    }

    return render_template('games.html', **context)



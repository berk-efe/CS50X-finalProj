import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import DEFAULT_SHOPS
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
    if request.args.get('limit'):
        limit = int(request.args.get('limit'))
    else:
        limit = 15
        
    if request.args.get('sort'):
        sort = request.args.get('sort')
    else:
        sort = '-trending'
        
    if request.args.get('shops'):
        shops = request.args.getlist('shops')
        shops = list(map(int, shops))
    else:
        shops = DEFAULT_SHOPS

    if request.args.get("price"):
        price = int(request.args.get("price"))
    else:
        price = None

    if request.args.get("cut"):
        cut = int(request.args.get("cut"))
    else:
        cut = None

    deals = get_deals(sort=sort, limit=limit, shops=shops, max_price=price, min_cut=cut)
    
    context = {
        'deals': deals
    }

    return render_template('games.html', **context)

@app.route('/about')
def about():
    return render_template('about.html')

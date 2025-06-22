import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import DEFAULT_SHOPS
from helper import get_deals, login_required

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///keepTrack.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("must provide username", "danger")
            return redirect("/register")

        elif not email:
            flash("must provide email", "danger")
            return redirect("/register")

        elif not password:
            flash("must provide password", "danger")
            return redirect("/register")
        
        elif not confirmation:
            flash("must provide confirmation", "danger")
            return redirect("/register")
        
        elif password != confirmation:
            flash("passwords do not match", "danger")
            return redirect("/register")
        
        try:
            db.execute(
                "INSERT INTO users(username, email, hash) VALUES(?,?,?)",
                username, email, generate_password_hash(password)
            )

            rows = db.execute(
                "SELECT * FROM users WHERE username = ?", username
            )

            session["user_id"] = rows[0]["id"]
            flash('Registration Complete!', 'success')
            return redirect('/')

        except ValueError as e:
            flash(f"Username already exists\n {e}", "danger")
            return redirect("/register")
        
    
    return render_template('register.html')


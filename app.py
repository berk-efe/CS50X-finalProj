import os


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import DEFAULT_SHOPS, db
from helper import get_deals, login_required, get_game_by_id

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.context_processor
def inject_globals():
    if 'user_id' in session:
        user = db.execute("SELECT * FROM users WHERE id = ?", session['user_id'])
        if user:
            return {'username': user[0]['username'], 'user': user[0]}
    else:
        return {}


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

    deals = get_deals(sort=sort, limit=limit, shops=shops, max_price=price, min_cut=cut, user_id=session.get('user_id'))
    
    user_id = session.get('user_id')
    
    
    context = {
        'deals': deals
    }

    return render_template('games.html', **context)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile/<username>')
@login_required
def profile(username):
    """Display user profile."""
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    if len(rows) != 1:
        flash("User not found.", "danger")
        return redirect("/")

    user = rows[0]

    # Fetch user's favorite game ids
    fav_ids = db.execute("SELECT game_id FROM favorites WHERE user_id = ?", user['id'])
    
    print(f"Favorite IDs for user {user['username']}: {fav_ids}")
    
    favs = []
    if fav_ids:
        fav_ids = [fav['game_id'] for fav in fav_ids]
        for id in fav_ids:
            game = get_game_by_id(game_id=id)
            favs.append(game)
            
    print(favs)
        
    context = {
        'user': user,
        'favs': favs
    }

    return render_template('profile.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username:
            flash("must provide username", "danger")
            return redirect("/login")
        elif not password:
            flash("must provide password", "danger")
            return redirect("/login")
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("invalid username and/or password", "danger")
            return redirect("/login")
        
        session["user_id"] = rows[0]["id"]
        flash("Logged in successfully.", "success")
        return redirect("/")
    
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

@app.route('/logout')
@login_required
def logout():
    """Log user out."""
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect("/")

@app.route('/post/favorite', methods=['POST'])
@login_required
def post_favorite():
    """Add a game to favorites."""
    game_id = request.form.get("game_id")
    
    if not game_id:
        flash("Game ID is required.", "danger")
        return redirect("/games")

    user_id = session['user_id']
    
    # Check if the game is already favorited
    existing_fav = db.execute("SELECT * FROM favorites WHERE user_id = ? AND game_id = ?", user_id, game_id)
    
    if existing_fav:
        flash("Game is already in your favorites.", "info")
        return redirect("/games")
    
    # Insert the favorite
    db.execute("INSERT INTO favorites (user_id, game_id) VALUES (?, ?)", user_id, game_id)
    flash("Game added to favorites!", "success")
    
    return redirect("/games")


@app.route('/post/unfavorite', methods=['POST'])
@login_required
def post_unfavorite():
    """Remove a game from favorites."""
    game_id = request.form.get("game_id")
    
    if not game_id:
        flash("Game ID is required.", "danger")
        return redirect("/games")

    user_id = session['user_id']
    
    # Check if the game is favorited
    existing_fav = db.execute("SELECT * FROM favorites WHERE user_id = ? AND game_id = ?", user_id, game_id)
    
    if not existing_fav:
        flash("Game is not in your favorites.", "info")
        return redirect("/games")
    
    # Delete the favorite
    db.execute("DELETE FROM favorites WHERE user_id = ? AND game_id = ?", user_id, game_id)
    flash("Game removed from favorites!", "success")
    
    return redirect("/games")

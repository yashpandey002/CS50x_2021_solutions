import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session['user_id']
    shr_info = db.execute(
        "SELECT shr_symbol, shr_name, shr_price, SUM(shr_qty) as shr_qty FROM user_transactions WHERE user_id = ? AND shr_qty > 0 GROUP BY shr_symbol", user_id)

    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash[0]["cash"]

    total_cash = cash

    for row in shr_info:
        total_cash += row["shr_qty"] * row["shr_price"]

    return render_template("index.html", shr_info=shr_info, usd=usd, cash=cash, total_cash=total_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    user_id = session['user_id']

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Must provide symbol", 400)

        stock = lookup(symbol)
        if stock == None:
            return apology("Invalid symbol", 400)

        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("Invalid shares", 400)
        except:
            return apology("Missing shares", 400)

        price = stock['price']
        name = stock['name']
        purchase_value = price * shares

        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash[0]["cash"]

        if(purchase_value > cash):
            return apology("Out of Cash", 400)

        db.execute("INSERT INTO user_transactions(user_id, shr_name, shr_symbol, shr_qty, shr_price, trans_type) VALUES(?, ?, ?, ?, ?, ?)", user_id, name, symbol, shares, price, "BUY")

        db.execute("UPDATE users SET cash = ?", cash - purchase_value)
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session['user_id']
    data = db.execute("SELECT shr_symbol, shr_qty, shr_price, time FROM user_transactions WHERE user_id = ?", user_id)
    return render_template("history.html", data=data, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/reset-password", methods=["GET", "POST"])
@login_required
def reset_psswrd():
    """Let user change the password"""
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("reset-psswrd.html")

    if request.method == "POST":
        new_password = request.form.get("new_password")
        if not new_password:
            return apology("New password is missing")

        confirm_password = request.form.get("confirmation")
        if not confirm_password:
            return apology("New password is missing")
        if new_password != confirm_password:
            return apology("Passwords didn't match!", 400)

        password_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password, user_id)
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Enter a symbol", 400)
        info = lookup(symbol)
        if info == None:
            return apology("Invalid symbol of share", 400)

        return render_template("quoted.html", stock=info, usd=usd)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Please input username", 400)

        password = request.form.get("password")
        if not password:
            return apology("Please input password", 400)

        confirm_pswd = request.form.get("confirmation")
        if not confirm_pswd:
            return apology("Please confirm password", 400)

        if password != confirm_pswd:
            return apology("Password didn't match", 400)

        password_hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, password_hash)
            return redirect("/login")
        except:
            return apology("Username already used!", 400)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    if request.method == "POST":
        symbols_db = db.execute("SELECT shr_symbol FROM user_transactions WHERE user_id = ? GROUP BY shr_symbol", user_id)
        symbols = []
        for row in symbols_db:
            symbols.append((row['shr_symbol']))

        symbol = request.form.get("symbol")
        if not symbol or (symbol not in symbols):
            return apology("Invalid symbol", 400)

        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("Invalid shares", 400)

            shares_in_DB = db.execute(
                "SELECT SUM(shr_qty) as shr_qty FROM user_transactions WHERE user_id = ? AND shr_symbol = ? GROUP BY shr_symbol", user_id, symbol)[0]['shr_qty']
            if shares > shares_in_DB:
                return apology("To many shares", 400)
        except:
            return apology("Missing shares", 400)

        stock = lookup(symbol)
        price = stock['price']
        name = stock['name']
        sell_value = price * shares

        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", current_cash + sell_value, user_id)

        db.execute("INSERT INTO user_transactions(user_id, shr_symbol, shr_name, shr_price, shr_qty, trans_type) VALUES(?, ?, ?, ?, ?, ?)",
        user_id, symbol, name, price, -shares, "SELL")
        return redirect("/")

    else:
        symbols = db.execute("SELECT shr_symbol FROM user_transactions WHERE user_id = ? GROUP BY shr_symbol", user_id)
        return render_template("sell.html", symbols=symbols)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)






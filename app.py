import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Flask,
    flash,
    session,
    render_template,
    request,
    redirect,
    url_for,
)
from sqlalchemy import func
from datetime import datetime
import plotly.graph_objects as go

from models import db, User, Transaction, Account, Category
from helpers import get_categories_statistics, create_pie_chart

# Initialize Flask application
app = Flask(__name__)

# Configure the database URI and secrey key for sessions
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///budgeteer.db"
)
app.config["SECRET_KEY"] = "mysecretkey"

# Initialize database
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all(checkfirst=True)

# List of month names for referencing
MONTHS = [
    "January",
    "Ferbuary",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


# Prevent caching of pages
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    return response


# Ensure user has authorization before acessing all protected pages
@app.before_request
def check_login():
    if "user_id" not in session and request.endpoint not in ["index", "static"]:
        return redirect(url_for("index"))


# Guarantee that session is available in all templates
@app.context_processor
def inject_session():
    return dict(session=session)


# Route for welcome page where users can log in or register
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        action = request.form.get("action")

        if action == "login":
            # Extract login data
            username = request.form["username"]
            password = request.form["password"]

            # Verify blank fields
            if not username or not password:
                flash("Required fields are missing.")
                return redirect(url_for("index", form="login"))

            # Check if user exists
            user = User.query.filter_by(username=username).first()

            # Verify password
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["username"] = user.username
                return redirect(url_for("financial_log"))
            else:
                flash("Invalid credentials.")
                return redirect(url_for("index", form="login"))

        elif action == "register":
            # Extract login data
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            confirmation = request.form["confirmation"]

            # Verify blank fields
            if not username or not password or not password or not confirmation:
                flash("Required fields are missing.")
                return redirect(url_for("index", form="register"))

            # Check if email, username already exists and if passwords match
            if User.query.filter_by(email=email).first():
                flash("Email already exists.")
                return redirect(url_for("index", form="register"))

            if User.query.filter_by(username=username).first():
                flash("Username already exists.")
                return redirect(url_for("index", form="register"))

            if password != confirmation:
                flash("Passwords do not match.")
                return redirect(url_for("index", form="register"))

            # Hash the password for storing in database
            hashed_password = generate_password_hash(password)

            # Create new user
            new_user = User(
                username=username, email=email, password=hashed_password
            )

            # Add user entry to database and commit change
            db.session.add(new_user)
            db.session.commit()

            # Store user ID and name in session
            session["user_id"] = new_user.id
            session["username"] = new_user.username

            return redirect(url_for("financial_log"))

    return render_template("index.html")


# Route for logging out user
@app.route("/logout")
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for("index"))


# Route for managing transactions
@app.route("/financial_log", methods=["GET", "POST"])
def financial_log():
    # Fetch user id, registered accounts and categories
    user_id = session.get("user_id")
    accounts = Account.query.filter_by(user_id=user_id).all()
    categories = Category.query.filter_by(user_id=user_id).all()

    # Extract current date
    date = datetime.now()
    year = date.year
    month = date.month

    if request.method == "POST":
        action = request.form.get("action")

        if action == "filter":
            # Extract date data and convert month name to corresponding index in MONTHS
            year = request.form["year"]
            month = MONTHS.index(request.form["month"]) + 1

        if action == "add_entry":
            # Extract transaction data
            tsct_type = request.form["transaction_type"]
            tsct_acc = request.form.get("transaction_account")
            tsct_value = request.form["transaction_value"]
            tsct_dtl = request.form["transaction_details"]
            tsct_ctg = request.form.get("transaction_category")
            tsct_date = request.form["transaction_date"]

            if tsct_date:
                tsct_date = datetime.strptime(tsct_date, "%Y-%m-%d").date()

            if (
                not tsct_value
                or not tsct_dtl
                or not tsct_date
                or not tsct_acc
                or not tsct_ctg
                or not tsct_type
            ):
                flash("All fields are required.")
            else:
                # Create a new transaction
                new_tsct = Transaction(
                    type=tsct_type,
                    details=tsct_dtl,
                    date=tsct_date,
                    value=tsct_value,
                    category_id=tsct_ctg,
                    account_id=tsct_acc,
                )

                # Add new transaction to database
                db.session.add(new_tsct)

                # Update account balance according to transaction type
                account = Account.query.get(tsct_acc)
                if account:
                    if tsct_type == "Income":
                        account.balance += float(tsct_value)
                    elif tsct_type == "Expense":
                        account.balance -= float(tsct_value)

                # Commit changes in database
                db.session.commit()

    # Fetch total balance of accounts
    total_balance = (
        db.session.query(func.sum(Account.balance))
        .filter_by(user_id=user_id)
        .scalar()
    ) or 0.0

    # Fetch transactions for the current date or the filtered date
    transactions = (
        db.session.query(Transaction, Account, Category)
        .join(Account, Account.id == Transaction.account_id)
        .join(Category, Category.id == Transaction.category_id)
        .filter(
            Account.user_id == user_id,
            func.extract("year", Transaction.date) == year,
            func.extract("month", Transaction.date) == month,
        )
        .order_by(Transaction.date.desc())
        .all()
    )

    return render_template(
        "financial_log.html",
        months=MONTHS,
        current_year=year,
        current_month=MONTHS[month - 1],
        accounts=accounts,
        categories=categories,
        transactions=transactions,
        total_balance=total_balance,
    )


# Route for managing user accounts
@app.route("/accounts", methods=["GET", "POST"])
def accounts():

    # Fetch user id, registered accounts, categories and balance
    user_id = session.get("user_id")
    accounts = Account.query.filter_by(user_id=user_id).all()
    categories = Category.query.filter_by(user_id=user_id).all()
    total_balance = (
        db.session.query(func.sum(Account.balance))
        .filter_by(user_id=user_id)
        .scalar()
    ) or 0.0

    if request.method == "POST":

        # Extract form data
        acc_type = request.form["account_type"]
        acc_bank = request.form["account_bank"]
        acc_name = request.form["account_name"]

        # Validate category name
        if not acc_name:
            flash("Account name is required.")
            return redirect(url_for("accounts", show_modal="add_account"))

        # Create new account
        new_account = Account(
            type=acc_type, bank=acc_bank, name=acc_name, user_id=user_id
        )

        # Add account to database and commit changes
        db.session.add(new_account)
        db.session.commit()

        return redirect(url_for("accounts"))

    return render_template(
        "accounts.html",
        accounts=accounts,
        categories=categories,
        total_balance=total_balance,
    )


# Route for generating monthly reports
@app.route("/reports", methods=["GET", "POST"])
def reports():
    # Fetch user id, registered accounts, categories and balance
    user_id = session.get("user_id")
    accounts = Account.query.filter_by(user_id=user_id).all()
    categories = Category.query.filter_by(user_id=user_id).all()
    total_balance = (
        db.session.query(func.sum(Account.balance))
        .filter_by(user_id=user_id)
        .scalar()
    ) or 0.0

    date = datetime.now()
    year = date.year
    month = date.month
    transaction_type = "Expense"

    if request.method == "POST":
        year = request.form["year"]
        month = MONTHS.index(request.form["month"]) + 1
        transaction_type = request.form["tsct_type"]

    # Get categories statistics for generating chart
    categories_statistics = get_categories_statistics(
        user_id, year, month, transaction_type
    )

    # Generate chart based on category statistics
    pie_chart_html = (
        create_pie_chart(categories_statistics)
        if categories_statistics
        else None
    )

    return render_template(
        "reports.html",
        year=year,
        month=MONTHS[month - 1],
        months=MONTHS,
        type=transaction_type,
        accounts=accounts,
        categories=categories,
        statistics=categories_statistics,
        total_balance=total_balance,
        pie_chart_html=pie_chart_html,
    )


# Route for creating categories
@app.route("/categories", methods=["POST"])
def categories():

    # Fetch user id from session
    user_id = session.get("user_id")

    if request.method == "POST":

        # Fetch form data
        ctg_name = request.form["category_name"]

        # Validate category name
        if not ctg_name:
            flash("Category name is required.")
            return redirect(request.referrer + "?show_modal=add_category")

        # Create new category
        new_category = Category(name=ctg_name, user_id=user_id)

        # Add category to database and commit changes
        db.session.add(new_category)
        db.session.commit()

        return redirect(request.referrer)

    return redirect(request.referrer)

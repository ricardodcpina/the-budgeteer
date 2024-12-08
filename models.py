from flask_sqlalchemy import SQLAlchemy

"""
Creates database instance and models for the web app using SQLAlchemy lib
"""

# Create a SQLAlchemy database instance
db = SQLAlchemy()

# Defines User model - represents an individual user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    accounts = db.relationship("Category", backref="user", lazy=True)
    categories = db.relationship("Account", backref="user", lazy=True)

# Defines Transaction model - represents the financial transactions
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    details = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    value = db.Column(db.Float(), nullable=False)
    account_id = db.Column(
        db.Integer, db.ForeignKey("account.id"), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False
    )

# Defines Account model - represents a financial instituition account
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(40), nullable=False)
    bank = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship("Transaction", backref="account", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Defines Category model - represents a group of transactions
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    transactions = db.relationship("Transaction", backref="category", lazy=True)

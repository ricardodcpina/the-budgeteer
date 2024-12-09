from flask import session
from sqlalchemy import func
from datetime import datetime
import plotly.graph_objects as go
from models import db, Transaction, Category, Account

"""
Defines some helper functions used in app.py
"""


def get_categories_statistics(
    user_id,
    year,
    month,
    transaction_type,
):
    """
    Fetch the relevant transaction data grouped by category to be displayed in the pie chart
    """

    # Fetch category names and amounts based on filters
    category_amounts = (
        db.session.query(
            Category.name.label("category_name"),
            func.sum(Transaction.value).label("total_value"),
        )
        .join(Transaction, Transaction.category_id == Category.id)
        .join(Account, Account.id == Transaction.account_id)
        .filter(
            Account.user_id == user_id,
            Transaction.type == transaction_type,
            func.extract("year", Transaction.date) == year,
            func.extract("month", Transaction.date) == month,
        )
        .group_by(Category.name)
        .all()
    )

    # Check if data is empty
    if category_amounts.__len__() == 0:
        return None

    # Calculate month total based on each category
    monthly_total = sum(
        category_row.total_value for category_row in category_amounts
    )

    # Create statistics for each listed category
    categories_statistics = []
    for category_row in category_amounts:
        percentage = (
            (category_row.total_value / monthly_total) * 100
            if monthly_total > 0
            else 0
        )
        categories_statistics.append(
            {
                "category_name": category_row.category_name,
                "total_value": category_row.total_value,
                "percentage": percentage,
            }
        )

    return categories_statistics


def create_pie_chart(statistics):
    """
    Creates the pie chart with the transactions grouped by category
    """

    # Prepare the data for pie chart
    pie_chart_data = {
        "labels": [transaction["category_name"] for transaction in statistics],
        "values": [transaction["total_value"] for transaction in statistics],
        "percentages": [
            transaction["percentage"] for transaction in statistics
        ],
    }

    # Create the pie chart using Plotly lib
    fig = go.Figure(
        data=[
            go.Pie(
                labels=pie_chart_data["labels"],
                values=pie_chart_data["values"],
                hole=0.3,
                textfont=dict(size=16),
                hovertemplate="%{label}: <b>$%{value:,.2f}</b><br>Percentage: %{percent:.2%}<extra></extra>",
            )
        ]
    )

    # Customize chart layout
    fig.update_layout(
        autosize=True,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(
            font=dict(size=18),
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5,
        ),
        hoverlabel=dict(
            font=dict(size=20),
        ),
    )

    # Convert to HTML format
    pie_chart_html = fig.to_html(full_html=False)

    return pie_chart_html

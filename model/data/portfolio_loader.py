import pandas as pd

from model.policy import Policy
from model.portfolio import Portfolio
from model.data.portfolio_validation import validate_required_columns

def row_to_policy(row):
    """
    Convert a dataframe row into a Policy object.
    """

    return Policy(
        age=int(row["age"]),
        term=int(row["term"]),
        sum_assured=float(row["sum_assured"]),
        premium=float(row["premium"]),
        weight=int(row.get("weight", 1)),
        gender=row.get("gender", "M"),
        smoker_status=row.get("smoker_status", "Non-Smoker"),
        product_type=row.get("product_type", "Term"),
    )

def dataframe_to_policies(df):
    """
    Convert dataframe into a list of Policy objects.
    """

    validate_required_columns(df)

    return [
        row_to_policy(row)
        for _, row in df.iterrows()
    ]

def load_portfolio_csv(path):
    """
    Load portfolio from CSV file.
    """

    df = pd.read_csv(path)

    policies = dataframe_to_policies(df)

    return Portfolio(policies)
import pandas as pd
from model.results import ValuationResult


def build_profit_dataframe(result: ValuationResult):
    """
    Converts structured valuation output into tabular form for analysis and visualization.

    """

    if result.breakdown is None:
        raise ValueError("ValuationResult does not contain breakdown. Set return_breakdown=True.")

    return pd.DataFrame(
    [row.to_dict() for row in result.breakdown]
)


def add_profit_signature(df):
    """
    Profit signature shows how total profit is distributed over time.

    """

    total_profit = df["pv_net"].sum()

    df = df.copy()

    df["profit_pct"] = df["pv_net"] / total_profit

    return df


def summary_metrics(df):
    """
    Provides high-level summary statistics for quick interpretation.
    
    """

    return {
        "total_pv_profit": df["pv_net"].sum(),
        "total_cash_profit": df["net_cashflow"].sum(),
        "peak_profit_year": df.loc[df["pv_net"].idxmax(), "t"]
    }
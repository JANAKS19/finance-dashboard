import pandas as pd


def load_data(path):
    return pd.read_csv(path, parse_dates=['date'])


def filter_by_date(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    return df[
        (df['date'] >= start_date) &
        (df['date'] <= end_date)
    ]


def summary_metrics(df):
    income = df[df['type'] == 'income']['amount'].sum()
    expense = df[df['type'] == 'expense']['amount'].sum()
    net = income - expense
    return income, expense, net



def daily_time_series(df):
    """
    Prepare daily income, expense, and cumulative net income
    """

    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    # Daily aggregation
    daily = (
        df.groupby(['date', 'type'])['amount']
        .sum()
        .reset_index()
    )

    # Pivot to wide format
    pivot = daily.pivot(
        index='date',
        columns='type',
        values='amount'
    ).fillna(0)

    # Ensure columns exist
    pivot['income'] = pivot.get('income', 0)
    pivot['expense'] = pivot.get('expense', 0)

    # Net income (daily)
    pivot['net_income'] = pivot['income'] - pivot['expense']

    # ✅ CUMULATIVE NET (KEY LINE)
    pivot['net_income_cumulative'] = pivot['net_income'].cumsum()

    return pivot.reset_index()


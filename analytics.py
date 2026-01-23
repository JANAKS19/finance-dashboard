def daily_time_series(df):
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])

    daily = (
        df.groupby(['date', 'type'])['amount']
        .sum()
        .reset_index()
    )

    pivot = daily.pivot(
        index='date',
        columns='type',
        values='amount'
    ).fillna(0)

    pivot['net_income'] = pivot.get('income', 0) - pivot.get('expense', 0)

    # 🔥 ADD THIS LINE (KEY)
    pivot['net_income_cumulative'] = pivot['net_income'].cumsum()

    return pivot.reset_index()

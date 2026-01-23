import plotly.express as px


def expense_pie_chart(df):
    expense_df = df[df['type'] == 'expense']

    fig = px.pie(
        expense_df,
        names='category',
        values='amount',
        title='Expense Distribution (%)',
        hole=0.4
    )

    fig.update_traces(textinfo='percent+label')
    return fig


def income_pie_chart(df):
    income_df = df[df['type'] == 'income']

    fig = px.pie(
        income_df,
        names='category',
        values='amount',
        title='Income Distribution (%)',
        hole=0.4
    )

    fig.update_traces(textinfo='percent+label')
    return fig


def time_series_chart(df):
    """
    df must contain:
    date, income, expense, net_income_cumulative
    """

    fig = px.line(
        df,
        x="date",
        y=["income", "expense", "net_income_cumulative"],
        labels={
            "value": "Amount",
            "variable": "Metric"
        },
        title="Income vs Expense vs Net Income Over Time"
    )

    fig.update_layout(
        legend_title_text="",
        hovermode="x unified"
    )

    return fig
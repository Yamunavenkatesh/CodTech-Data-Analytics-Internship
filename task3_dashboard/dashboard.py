import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("../Datasets/sales_data_sample.csv", encoding='latin1')

# Convert date column
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])

# Initialize app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([

    html.H1("📊 Sales Dashboard", style={"textAlign": "center"}),

    # Dropdown
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in df["COUNTRY"].unique()],
        value=df["COUNTRY"].unique()[0],
        clearable=False
    ),

    html.Br(),

    # KPI
    html.Div(id="total-sales", style={"fontSize": 24, "textAlign": "center"}),

    html.Br(),

    # Graphs
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="line-chart"),
    dcc.Graph(id="pie-chart")

])

# Callback (THIS MAKES IT INTERACTIVE)
@app.callback(
    Output("bar-chart", "figure"),
    Output("line-chart", "figure"),
    Output("pie-chart", "figure"),  
    Output("total-sales", "children"),
    Input("country-dropdown", "value")  
)
def update_dashboard(selected_country):

    filtered_df = df[df["COUNTRY"] == selected_country]

    # Bar chart
    bar_fig = px.bar(
        filtered_df,
        x="PRODUCTLINE",
        y="SALES",
        title="Sales by Product Line",
        color_discrete_sequence=["#4CAF50"]
    )

    # Line chart
    line_data = filtered_df.groupby("ORDERDATE")["SALES"].sum().reset_index()

    line_fig = px.line(
        line_data,
        x="ORDERDATE",
        y="SALES",
        title="Sales Over Time",
        color_discrete_sequence=["#FF6F00"]
    )
    pie_fig = px.pie(
    filtered_df,
    names="PRODUCTLINE",
    values="SALES",
    title="Sales Distribution by Product Line",
    color_discrete_sequence=["#4CAF50", "#FF6F00", "#2196F3", "#9C27B0", "#FFC107"]
    )

    # KPI
    total_sales = filtered_df["SALES"].sum()

    return bar_fig, line_fig, pie_fig, f"💰 Total Sales: {total_sales:,.2f}"

# Run app
if __name__ == "__main__":
    app.run(debug=True)
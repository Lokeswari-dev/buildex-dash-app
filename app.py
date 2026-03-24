import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os # 1. Ee line add cheshanu

# Initialize app with FLATLY theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Create Scorecard Function
def create_scorecard(title, value_id, text_color="primary"):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title text-muted text-uppercase text-center"),
            html.H2(id=value_id, className=f"card-text text-center text-{text_color}")
        ]),
        className="shadow-sm mb-4"
    )

app.layout = dbc.Container([
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
    
    html.Div([
        html.H1("Buildex India Sales - Advanced Analytics", className="text-center text-primary fw-bold display-4 mb-2"),
        html.Hr(className="my-4")
    ], className="mt-4"),
    
    dbc.Row([
        dbc.Col(create_scorecard("Total Revenue", 'total-revenue-kpi', "success"), md=4),
        dbc.Col(create_scorecard("Pending Amount", 'pending-amount-kpi', "warning"), md=4),
        dbc.Col(create_scorecard("Total Order Count", 'order-count-kpi', "info"), md=4),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart-location'), md=7),
        dbc.Col(dcc.Graph(id='pie-chart-status'), md=5),
    ]),
], fluid=True, className="p-4")

@app.callback(
    [Output('total-revenue-kpi', 'children'),
     Output('pending-amount-kpi', 'children'),
     Output('order-count-kpi', 'children'),
     Output('bar-chart-location', 'figure'),
     Output('pie-chart-status', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n_intervals):
    try:
        # 2. Corrected Google Sheet Link (removed extra 'S')
        sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQjA3P7sFrty1FPvJSeEJTN-bKvmYfdkZT2Wj4EULb_Q7nUC4NpjBMiTgqAFTmEZmVljPE2Ze7IwX4s/pub?gid=0&single=true&output=csv'
        df = pd.read_csv(sheet_url)
    except Exception as e:
        print(f"Error loading data: {e}")
        df = pd.DataFrame()
        
    if df.empty:
        return "₹ 0.00", "₹ 0.00", "0", px.bar(title="No Data"), px.pie(title="No Data")
        
    # Data Calculation
    total_revenue = df['Revenue'].sum() if 'Revenue' in df.columns else 0
    pending_amount = df[df['Payment Status'] == 'Pending']['Revenue'].sum() if 'Payment Status' in df.columns else 0
    order_count = len(df)
    
    rev_str = f"₹ {total_revenue:,.2f}"
    pending_str = f"₹ {pending_amount:,.2f}"
    count_str = f"{order_count:,}"

    # Visuals
    fig_bar = px.bar(df, x='Location', y='Revenue', color='Material', barmode='group', title='Revenue by Location & Material') if 'Location' in df.columns else px.bar(title="No Data")
    fig_pie = px.pie(df, names='Payment Status', values='Revenue', title='Revenue by Payment Status') if 'Payment Status' in df.columns else px.pie(title="No Data")
        
    return rev_str, pending_str, count_str, fig_bar, fig_pie

if __name__ == '__main__':
    # 3. Use Render's dynamic port
    port = int(os.environ.get("PORT", 10000))
    app.run_server(host='0.0.0.0', port=port, debug=False)

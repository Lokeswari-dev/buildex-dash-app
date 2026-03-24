import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Initialize app with FLATLY theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

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
    # Interval Component
    dcc.Interval(
        id='interval-component',
        interval=5000, # 5 seconds
        n_intervals=0
    ),
    
    # Header
    html.Div([
        html.H1("Buildex India Sales - Advanced Analytics", className="text-center text-primary fw-bold display-4 mb-2"),
        html.Hr(className="my-4")
    ], className="mt-4"),
    
    # Scorecards Row
    dbc.Row([
        dbc.Col(create_scorecard("Total Revenue", 'total-revenue-kpi', "success"), md=4),
        dbc.Col(create_scorecard("Pending Amount", 'pending-amount-kpi', "warning"), md=4),
        dbc.Col(create_scorecard("Total Order Count", 'order-count-kpi', "info"), md=4),
    ]),
    
    # Charts Row
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
    # Load data dynamically
    try:
        df = pd.read_csv('buildex_data.csv')
    except Exception:
        # Fallback empty state if file is unavailable
        df = pd.DataFrame()
        
    if df.empty:
        return "₹ 0.00", "₹ 0.00", "0", px.bar(title="No Data"), px.pie(title="No Data")
        
    # Calculate KPIs
    total_revenue = df['Revenue'].sum() if 'Revenue' in df.columns else 0
    
    # Handle pending amount safely
    if 'Payment Status' in df.columns and 'Revenue' in df.columns:
        pending_amount = df[df['Payment Status'] == 'Pending']['Revenue'].sum()
    else:
        pending_amount = 0
        
    order_count = len(df)
    
    # Format KPIs
    rev_str = f"₹ {total_revenue:,.2f}"
    pending_str = f"₹ {pending_amount:,.2f}"
    count_str = f"{order_count:,}"

    # Grouped Bar Chart: Revenue by Location
    if 'Location' in df.columns and 'Revenue' in df.columns:
        if 'Material' in df.columns:
            bar_df = df.groupby(['Location', 'Material'], as_index=False)['Revenue'].sum()
            fig_bar = px.bar(
                bar_df,
                x='Location',
                y='Revenue',
                color='Material',
                barmode='group',
                title='Revenue by Location & Material'
            )
        else:
            bar_df = df.groupby('Location', as_index=False)['Revenue'].sum()
            fig_bar = px.bar(
                bar_df,
                x='Location',
                y='Revenue',
                title='Revenue by Location'
            )
    else:
        fig_bar = px.bar(title="Revenue Data Unavailable")

    # Pie Chart: Payment Status
    if 'Payment Status' in df.columns and 'Revenue' in df.columns:
        pie_df = df.groupby('Payment Status', as_index=False)['Revenue'].sum()
        fig_pie = px.pie(
            pie_df,
            names='Payment Status',
            values='Revenue',
            title='Revenue by Payment Status'
        )
    else:
        fig_pie = px.pie(title="Payment Status Data Unavailable")
        
    return rev_str, pending_str, count_str, fig_bar, fig_pie

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

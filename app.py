import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import os 

# Initialize app with FLATLY theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# Fetch initial data for dropdowns
sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQjA3P7sFrty1FPvJSeEJTN-bKvmYfdkZT2Wj4EULb_Q7nUC4NpjBMiTgqAFTmEZmVljPE2Ze7IwX4s/pub?gid=0&single=true&output=csv'
try:
    init_df = pd.read_csv(sheet_url)
    locations = sorted([str(x) for x in init_df['Location'].dropna().unique()]) if 'Location' in init_df.columns else []
    materials = sorted([str(x) for x in init_df['Material'].dropna().unique()]) if 'Material' in init_df.columns else []
except Exception as e:
    print(f"Error loading initial data: {e}")
    locations = []
    materials = []

# Create Scorecard Function
def create_scorecard(title, value_id, text_color="primary"):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title text-muted text-uppercase text-center"),
            html.H2(id=value_id, className=f"card-text text-center text-{text_color}")
        ]),
        className="shadow-sm mb-4"
    )

sidebar = html.Div(
    [
        html.H3("Filters", className="display-6"),
        html.Hr(),
        html.P(
            "Filter the dashboard data:", className="lead"
        ),
        html.Div([
            html.Label("Location", className="fw-bold"),
            dcc.Dropdown(
                id='location-filter',
                options=[{'label': i, 'value': i} for i in locations],
                value=[],
                multi=True,
                placeholder="Select Location(s)..."
            ),
        ], className="mb-4"),
        html.Div([
            html.Label("Material", className="fw-bold"),
            dcc.Dropdown(
                id='material-filter',
                options=[{'label': i, 'value': i} for i in materials],
                value=[],
                multi=True,
                placeholder="Select Material(s)..."
            ),
        ], className="mb-4")
    ],
    className="bg-light p-4 shadow-sm",
    style={"height": "100%", "min-height": "100vh", "border-radius": "5px"}
)

content = html.Div(
    [
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
        
        html.Div([
            html.H3("Raw Data", className="mt-5 mb-3 text-secondary"),
            dash_table.DataTable(
                id='raw-data-table',
                columns=[],
                data=[],
                page_size=10,
                sort_action="native",
                filter_action="native",
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'sans-serif',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'Date'},
                        'minWidth': '150px'
                    }
                ],
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#f8f9fa'
                }
            )
        ]),
    ]
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, md=3),
        dbc.Col(content, md=9)
    ])
], fluid=True, className="p-3")

@app.callback(
    [Output('total-revenue-kpi', 'children'),
     Output('pending-amount-kpi', 'children'),
     Output('order-count-kpi', 'children'),
     Output('bar-chart-location', 'figure'),
     Output('pie-chart-status', 'figure'),
     Output('raw-data-table', 'data'),
     Output('raw-data-table', 'columns')],
    [Input('interval-component', 'n_intervals'),
     Input('location-filter', 'value'),
     Input('material-filter', 'value')]
)
def update_dashboard(n_intervals, selected_locations, selected_materials):
    try:
        # 2. Corrected Google Sheet Link (removed extra 'S')
        sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQjA3P7sFrty1FPvJSeEJTN-bKvmYfdkZT2Wj4EULb_Q7nUC4NpjBMiTgqAFTmEZmVljPE2Ze7IwX4s/pub?gid=0&single=true&output=csv'
        df = pd.read_csv(sheet_url)
    except Exception as e:
        print(f"Error loading data: {e}")
        df = pd.DataFrame()
        
    if df.empty:
        return "₹ 0.00M", "₹ 0.00M", "0", px.bar(title="No Data"), px.pie(title="No Data"), [], []
        
    # Apply Filters
    if selected_locations:
        df = df[df['Location'].isin(selected_locations)]
    if selected_materials:
        df = df[df['Material'].isin(selected_materials)]

    # Handle case where all data is filtered out
    if df.empty:
        return "₹ 0.00M", "₹ 0.00M", "0", px.bar(title="No Data Available for Selected Filters"), px.pie(title="No Data"), [], []

    # Data Calculation
    total_revenue = df['Revenue'].sum() if 'Revenue' in df.columns else 0
    pending_amount = df[df['Payment Status'] == 'Pending']['Revenue'].sum() if 'Payment Status' in df.columns else 0
    order_count = len(df)
    
    rev_str = f"₹ {total_revenue / 1_000_000:,.2f}M"
    pending_str = f"₹ {pending_amount / 1_000_000:,.2f}M"
    count_str = f"{order_count:,}"

    # Visuals
    fig_bar = px.bar(df, x='Location', y='Revenue', color='Material', barmode='group', title='Revenue by Location & Material') if 'Location' in df.columns else px.bar(title="No Data")
    fig_pie = px.pie(df, names='Payment Status', values='Revenue', title='Revenue by Payment Status') if 'Payment Status' in df.columns else px.pie(title="No Data")
        
    # Table Data
    table_df = df.copy()
    if 'Date' in table_df.columns:
        formatted_dates = pd.to_datetime(table_df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
        table_df['Date'] = formatted_dates.fillna(table_df['Date'])
    table_data = table_df.to_dict('records')
    table_columns = [{"name": i, "id": i} for i in table_df.columns]

    return rev_str, pending_str, count_str, fig_bar, fig_pie, table_data, table_columns

if __name__ == '__main__':
    # 3. Use Render's dynamic port
    port = int(os.environ.get("PORT", 10000))
    app.run_server(host='0.0.0.0', port=port, debug=False)

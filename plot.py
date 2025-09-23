import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import datetime
import numpy as np
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('z_attempt20//Building_A.csv') #USER INPUT FOLDER.
#Data preparation
df['record_timestamp'] = pd.to_datetime(df['record_timestamp'], format='%Y-%m-%d %H:%M:%S')
# df['record_timestamp'] = pd.to_datetime(df['record_timestamp'], format='%d/%m/%Y %H:%M') # summary table

df.dropna(inplace=True)
# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Chiller analysis Dashboard"

# Define chiller names and parameters
chillers = ['CHR-01', 'CHR-02', 'CHR-03', 'CHR-04']
parameters = ['CHWSWT', 'CHWRWT', 'CHWFWR', 'KW', 'Q']
param_names = {
    'CHWSWT': 'Chilled Water Supply Temperature (°C)',
    'CHWRWT': 'Chilled Water Return Temperature (°C)',
    'CHWFWR': 'Chilled Water Flow Rate (L/s)',
    'KW': 'Power Consumption (kW)',
    'Q': 'Cooling Capacity (kW)'
}
# Get all available column names for dropdowns
all_columns = [col for col in df.columns if col != 'record_timestamp']

# App layout
app.layout = html.Div([
    html.H1("Chiller Performance Monitoring Dashboard", 
            style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div([
        html.Div([
            html.Label("Select Chiller:"),
            dcc.Dropdown(
                id='chiller-dropdown',
                options=[{'label': chiller, 'value': chiller} for chiller in chillers],
                value='CHR-01',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Select Parameter:"),
            dcc.Dropdown(
                id='parameter-dropdown',
                options=[{'label': param_names[param], 'value': param} for param in parameters],
                value='CHWSWT',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Date Range:"),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=df['record_timestamp'].min(),
                end_date=df['record_timestamp'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    dcc.Graph(id='time-series-plot'),
    
    html.Div([
        html.Div([
            html.H3("Summary Statistics", style={'textAlign': 'center'}),
            html.Div(id='summary-stats')
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            dcc.Graph(id='comparison-plot')
        ], style={'width': '70%', 'display': 'inline-block'})
    ]),
    
    # NEW: Dual Parameter Comparison Section
    html.Hr(),
    html.H2("Dual Parameter Comparison (Normalized)", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '30px'}),
    
    html.Div([
        html.Div([
            html.Label("Select First Parameter:"),
            dcc.Dropdown(
                id='param1-dropdown',
                options=[{'label': col, 'value': col} for col in all_columns],
                value='CHR-01-CHWSWT',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Select Second Parameter:"),
            dcc.Dropdown(
                id='param2-dropdown',
                options=[{'label': col, 'value': col} for col in all_columns],
                value='CHR-01-CHWRWT',
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Normalization Method:"),
            dcc.RadioItems(
                id='normalization-method',
                options=[
                    {'label': 'Min-Max Scaling (0-1)', 'value': 'minmax'},
                    {'label': 'Z-Score Standardization', 'value': 'zscore'},
                    {'label': 'No Normalization', 'value': 'none'}
                ],
                value='minmax',
                inline=True
            )
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    dcc.Graph(id='dual-parameter-plot'),
    
    html.Div([
        html.Div([
            html.H4("Correlation Analysis", style={'textAlign': 'center'}),
            html.Div(id='correlation-stats')
        ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            dcc.Graph(id='scatter-plot')
        ], style={'width': '70%', 'display': 'inline-block'})
    ]),
    
    dcc.Graph(id='correlation-heatmap'),
    
    # NEW: Plot of selected column against time
    html.Hr(),
    html.H2("Plot of selected column against time",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '30px'}),
    html.Div([
        html.Div([
            html.Label("Select Column:"),
            dcc.Dropdown(
                id='single-column-dropdown',
                options=[{'label': col, 'value': col} for col in all_columns],
                value=all_columns[0],
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            html.Label("Normalization Method:"),
            dcc.RadioItems(
                id='single-column-normalization',
                options=[
                    {'label': 'Min-Max Scaling (0-1)', 'value': 'minmax'},
                    {'label': 'Z-Score Standardization', 'value': 'zscore'},
                    {'label': 'No Normalization', 'value': 'none'}
                ],
                value='none',
                inline=True
            )
        ], style={'width': '40%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    dcc.Graph(id='single-column-plot'),

    dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0
    )
], style={'padding': '20px'})

# Normalization functions
def normalize_data(data, method='minmax'):
    if method == 'minmax':
        scaler = MinMaxScaler()
        return scaler.fit_transform(data.values.reshape(-1, 1)).flatten()
    elif method == 'zscore':
        return (data - data.mean()) / data.std()
    else:  # no normalization
        return data

# Callbacks
@app.callback(
    [Output('time-series-plot', 'figure'),
     Output('summary-stats', 'children'),
     Output('comparison-plot', 'figure'),
     Output('dual-parameter-plot', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('correlation-stats', 'children'),
     Output('correlation-heatmap', 'figure'),
     Output('single-column-plot', 'figure')],
    [Input('chiller-dropdown', 'value'),
     Input('parameter-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('param1-dropdown', 'value'),
     Input('param2-dropdown', 'value'),
     Input('normalization-method', 'value'),
     Input('single-column-dropdown', 'value'),
     Input('single-column-normalization', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_dashboard(selected_chiller, selected_param, start_date, end_date, 
                    param1, param2, norm_method, selected_column, single_col_norm_method, n):
    # Filter data based on date range
    filtered_df = df[(df['record_timestamp'] >= start_date) & 
                    (df['record_timestamp'] <= end_date)].copy()
    
    # Time Series Plot
    col_name = f"{selected_chiller}-{selected_param}"
    ts_fig = px.line(filtered_df, x='record_timestamp', y=col_name,
                    title=f'{selected_chiller} - {param_names[selected_param]} Over Time')
    ts_fig.update_layout(
        xaxis_title='Time',
        yaxis_title=param_names[selected_param],
        hovermode='x unified'
    )
    
    # Summary Statistics
    current_data = filtered_df[col_name]
    stats = [
        html.P(f"Current Value: {current_data.iloc[-1]:.2f}"),
        html.P(f"Average: {current_data.mean():.2f}"),
        html.P(f"Minimum: {current_data.min():.2f}"),
        html.P(f"Maximum: {current_data.max():.2f}"),
        html.P(f"Standard Deviation: {current_data.std():.2f}")
    ]
    
    # Comparison Plot
    comp_fig = go.Figure()
    for chiller in chillers:
        comp_col = f"{chiller}-{selected_param}"
        comp_fig.add_trace(go.Scatter(
            x=filtered_df['record_timestamp'],
            y=filtered_df[comp_col],
            name=chiller,
            mode='lines'
        ))
    
    comp_fig.update_layout(
        title=f'Comparison: {param_names[selected_param]} Across All Chillers',
        xaxis_title='Time',
        yaxis_title=param_names[selected_param],
        hovermode='x unified'
    )
    
    # NEW: Dual Parameter Plot with Normalization
    if param1 in filtered_df.columns and param2 in filtered_df.columns:
        # Normalize data
        param1_norm = normalize_data(filtered_df[param1], norm_method)
        param2_norm = normalize_data(filtered_df[param2], norm_method)
        
        dual_fig = go.Figure()
        dual_fig.add_trace(go.Scatter(
            x=filtered_df['record_timestamp'],
            y=param1_norm,
            name=param1,
            mode='lines',
            line=dict(color='blue')
        ))
        dual_fig.add_trace(go.Scatter(
            x=filtered_df['record_timestamp'],
            y=param2_norm,
            name=param2,
            mode='lines',
            line=dict(color='red')
        ))
        
        norm_label = "Normalized Value" if norm_method != 'none' else "Original Value"
        dual_fig.update_layout(
            title=f'Dual Parameter Comparison: {param1} vs {param2}',
            xaxis_title='Time',
            yaxis_title=norm_label,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Scatter Plot
        scatter_fig = px.scatter(
            x=filtered_df[param1],
            y=filtered_df[param2],
            title=f'Scatter Plot: {param1} vs {param2}',
            labels={'x': param1, 'y': param2}
        )
        scatter_fig.update_traces(marker=dict(size=8, opacity=0.6))
        
        # Correlation Statistics
        correlation = filtered_df[param1].corr(filtered_df[param2])
        corr_stats = [
            html.H5(f"Correlation Analysis"),
            html.P(f"Correlation Coefficient: {correlation:.3f}"),
            html.P(f"Sample Size: {len(filtered_df)} points"),
            html.P(f"Parameter 1 Mean: {filtered_df[param1].mean():.2f}"),
            html.P(f"Parameter 2 Mean: {filtered_df[param2].mean():.2f}"),
            html.P(f"Parameter 1 Std: {filtered_df[param1].std():.2f}"),
            html.P(f"Parameter 2 Std: {filtered_df[param2].std():.2f}")
        ]
        
    else:
        dual_fig = go.Figure()
        scatter_fig = go.Figure()
        corr_stats = [html.P("Selected parameters not available in filtered data")]
    
    # Correlation Heatmap
    numeric_cols = [col for col in df.columns if col != 'record_timestamp' and col != 'season']
    corr_data = filtered_df[numeric_cols].corr()
    
    heat_fig = px.imshow(corr_data,
                        title='Correlation Heatmap Between All Parameters',
                        aspect='auto',
                        color_continuous_scale='RdBu_r')
    heat_fig.update_layout(height=600)
    
    # NEW: Single Column Plot
    y_data = normalize_data(filtered_df[selected_column], single_col_norm_method)
    y_axis_label = "Normalized Value" if single_col_norm_method != 'none' else selected_column
    
    single_col_fig = go.Figure()
    single_col_fig.add_trace(go.Scatter(
        x=filtered_df['record_timestamp'],
        y=y_data,
        name=selected_column,
        mode='lines'
    ))
    single_col_fig.update_layout(
        title=f'Plot of {selected_column} Over Time',
        xaxis_title='Time',
        yaxis_title=y_axis_label,
        hovermode='x unified'
    )
    
    return ts_fig, stats, comp_fig, dual_fig, scatter_fig, corr_stats, heat_fig, single_col_fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
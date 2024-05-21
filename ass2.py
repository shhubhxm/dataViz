import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('assign2_wastedata.csv')

# Parse the date column
df['Date'] = pd.to_datetime(df['Date'])

# Create the Dash app
app = dash.Dash(__name__)
app.title = "SCU Waste Data Visualization"

# Define the layout of the app
app.layout = html.Div([
    html.H1("Santa Clara University Waste Data Visualization", style={'text-align': 'center'}),

    html.Div([
        html.Label("Select Building:"),
        dcc.Dropdown(
            id='building-dropdown',
            options=[{'label': building, 'value': building} for building in df['Building'].unique()],
            value=df['Building'].unique()[0],
            multi=True
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Waste Stream:"),
        dcc.Dropdown(
            id='stream-dropdown',
            options=[{'label': stream, 'value': stream} for stream in df['Stream'].unique()],
            value=df['Stream'].unique()[0],
            multi=True
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='waste-line-graph'),
    dcc.Graph(id='waste-bar-graph'),

    html.Div(id='writeup', children=[
        html.H2("Design Rationale and Justification"),
        html.P("The interactive visualization allows users to explore waste data by building and waste stream. Different colors distinguish buildings and waste streams. Temporal trends are shown to identify patterns in waste management."),
        html.P("Users can interact with the dropdown menus to filter the data, making the visualization dynamic and informative. Annotations highlight significant events or policy changes affecting waste trends."),
        html.P("Bar charts provide a comparative view of total waste volumes, helping to identify high-impact areas for waste reduction."),
    ], style={'margin-top': '20px'})
])

# Define callback to update line graph
@app.callback(
    Output('waste-line-graph', 'figure'),
    [Input('building-dropdown', 'value'),
     Input('stream-dropdown', 'value')]
)
def update_line_graph(selected_buildings, selected_streams):
    filtered_df = df[df['Building'].isin(selected_buildings) & df['Stream'].isin(selected_streams)]
    fig = px.line(filtered_df, x='Date', y='Weight', color='Building', line_dash='Stream',
                  title='Waste Trends Over Time', labels={'Weight': 'Weight (lbs)'}, template='plotly_dark')
    fig.update_layout(legend_title_text='Building and Stream')
    return fig

# Define callback to update bar graph
@app.callback(
    Output('waste-bar-graph', 'figure'),
    [Input('building-dropdown', 'value'),
     Input('stream-dropdown', 'value')]
)
def update_bar_graph(selected_buildings, selected_streams):
    filtered_df = df[df['Building'].isin(selected_buildings) & df['Stream'].isin(selected_streams)]
    bar_df = filtered_df.groupby(['Building', 'Stream']).sum().reset_index()
    fig = px.bar(bar_df, x='Building', y='Weight', color='Stream', barmode='group',
                 title='Total Waste by Building and Stream', labels={'Weight': 'Total Weight (lbs)'}, template='plotly_dark')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

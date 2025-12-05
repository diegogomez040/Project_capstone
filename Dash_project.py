# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(URL)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Crete a dataframe with he name of sites
launch_sites_df = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={"textAlign": "center", "color": "#d35400", "font-size": 24}
            ),

        html.Div([
            html.Label("Select site:"),
            dcc.Dropdown(
                id='site-dropdown',
                options=[
                    {'label': 'ALL SITES', 'value': 'ALL'},
                    {'label': launch_sites_df[0], 'value': launch_sites_df[0]},
                    {'label': launch_sites_df[1], 'value': launch_sites_df[1]},
                    {'label': launch_sites_df[2], 'value': launch_sites_df[2]},
                    {'label': launch_sites_df[3], 'value': launch_sites_df[3]}
                ],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
            ),
        ]),

        html.Div([
            html.Label("Payload range (kg):"),
            dcc.RangeSlider(
                id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       2000: '2000',
                       4000: '4000',
                       6000: '6000',
                       8000: '8000',
                       10000: '10000'},
                value=[min_payload, max_payload])
        ]),

        html.Div(dcc.Graph(id='success-pie-chart', className='chart-grid', style={'display': 'flex'})),

        html.Div(dcc.Graph(id='success-payload-scatter-chart', className='chart-grid', style={'display': 'flex'}))])

# Function decorator to specify function input and output (piechart)
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby("Launch Site")["class"].value_counts().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df[filtered_df["Launch Site"]==entered_site], values='count',
        names='class',
        title=f'Total Success Launches fos site {entered_site}')
        return fig

# Function decorator to specify function input and output (scatterplot)
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property='value')])
def get_scatter_plot(entered_site, range_payload):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)']>=range_payload[0]) &
        (spacex_df['Payload Mass (kg)']<=range_payload[1])
        ]
    if entered_site=='ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Succes for all Sites',
            labels={
                'Payload Mass (kg)': 'Payload (kg)',
                'class': 'Launch Outcome (0=Fail, 1=Success)'
            }
        )
        return fig
    else:
        fig = px.scatter(
            filtered_df[filtered_df["Launch Site"]==entered_site],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Succes for {entered_site}',
            labels={
                'Payload Mass (kg)': 'Payload (kg)',
                'class': 'Launch Outcome (0=Fail, 1=Success)'
            }
        )
        return fig

if __name__ == '__main__':
    app.run(debug=True)
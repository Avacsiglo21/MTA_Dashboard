import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


mta_df = pd.read_csv("MTA_Daily_Ridership.csv",parse_dates=['Date'])

mta_df['Total Estimated Ridership'] = (mta_df['Subways: Total Estimated Ridership']+
                                       mta_df['Buses: Total Estimated Ridership']+
                                       mta_df['LIRR: Total Estimated Ridership']+
                                       mta_df['Metro-North: Total Estimated Ridership']+
                                       mta_df['Staten Island Railway: Total Estimated Ridership'])


external_stylesheets = [dbc.themes.MINTY]



radio_style = {
    'display': 'flex',
    'flex-direction': 'row',
    'justify-content': 'space-between',
    'padding': '5px',
    'border': '2px solid',
    'border-radius': '5px',
    'boxShadow': '3px 3px 3px rgba(10, 10, 10, 0.3)',
    'font-family': 'Aharoni, sans-serif',
    'font-size': '20px',
}

# Define the CSS style for the card
card_style = {
    'backgroundColor': '#ffffff',
    'padding': '5px',
    'borderRadius': '5px',
    'margin': '5px',
    'boxShadow': '3px 3px 3px rgba(10, 10, 10, 0.3)'
}

date_picker_style = {
    'backgroundColor': '#ffffff',
    'padding': '0px',
    'border': '2px solid #358f4d',
    'borderRadius': '5px',
    'margin': '0px',
    'boxShadow': '3px 3px 3px rgba(10, 10, 10, 0.3)',
    'width': '290px',
    'font-family': 'Aharoni, sans-serif',
    'font-size': '20px'


    
}


avg_card_style = {'backgroundColor': '#ffffff', 
                  'padding': '0px', 
                  'borderRadius': '5px', 
                  'margin': '0px', 
                  'font-family': 'Aharoni, sans-serif', 
                  'font-size': '18px', 
                  'boxShadow': '3px 3px 3px rgba(10, 10, 10, 0.3)', 
                  'text-align': 'center', 'font-weight': 'bold' }


app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "MTA Daily Ridership"

app.layout = dbc.Container([
    html.H2("MTA Data Dashboard: Analyzing Public Transport Trends", 
            style={'text-align': 'center', 'margin': '10px','padding': '10px'}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dcc.Checklist(
                    id='mta-checklist',
                    options=[
                        {'label': 'Subways', 'value': 'Subways'},
                        {'label': 'Buses', 'value': 'Buses'},
                        {'label': 'Long Island Rails', 'value': 'Long Island Rails'},
                        {'label': 'Metro-North', 'value': 'Metro-North'},
                        {'label': 'Staten Island Railway', 'value': 'Staten Island Railway'},
                        {'label': 'Access-A-Rid', 'value': 'Access-A-Rid'},
                        {'label': 'Bridges and Tunnels', 'value': 'Bridges and Tunnels'},
                    ],
                    value=['Subways','Buses', 'Bridges and Tunnels'],
                    style=radio_style, 
                ),
                dbc.Tooltip("Select the transportation modes you want to analyze.", target="mta-checklist", className="card border-primary mb-3")
            ], className="card border-primary mb-3"),
            dbc.Card([
                dcc.RadioItems(
                    id='date-radioitems',
                    options=[
                        {'label': 'Date', 'value': 'D'},
                        {'label': 'Week', 'value': 'W'},
                        {'label': 'Month', 'value': 'ME'},
                        {'label': 'Quarter', 'value': 'QE'},
                        {'label': 'Year', 'value': 'YE'}
                    ],
                    value='W',
                    inline=True,
                    style=radio_style
                ),
                dbc.Tooltip( "Choose the time interval for the data aggregation.", target="date-radioitems" )
            ], className="card border-primary mb-3"),
            
            dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=mta_df['Date'].min(),
                    end_date=mta_df['Date'].max(),
                    display_format='YYYY-MM-DD',
                    style=date_picker_style
                ),
            dbc.Tooltip( "Select the date range for the data analysis.", target="date-picker-range" ),

            html.Div(style={'margin': '20px'}),
            
            
        ]),
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(
                [dbc.CardHeader(html.H6("ESTIMATED RIDERSHIPS",
                                        style={'textAlign': 'left','padding': '0px','margin': '0px'})),
                 dbc.CardBody(
                     html.Div(id='avg-ridership', className='big-number'))
                    
                ],className="card text-white bg-primary mb-3", style=avg_card_style)),
        
        dbc.Tooltip("Average, minimum, and maximum values of ridership.", target="avg-ridership"),
        
        dbc.Col(dbc.Card(
                [dbc.CardHeader(html.H6("SCHEDULED TRIPS",
                                        style={'textAlign': 'center','padding': '0px','margin': '0px'})),
                 dbc.CardBody(
                     html.Div(id='avg-scheduled-trips', className='big-number'))
                    
                ],className="card text-white bg-primary mb-3", style=avg_card_style)),
        dbc.Tooltip("Average, minimum, and maximum values of scheduled trips.", target="avg-scheduled-trips"),
        
        dbc.Col(dbc.Card(
                [dbc.CardHeader(html.H6("TRAFFICS VOLUME",
                                        style={'textAlign': 'center','padding': '0px','margin': '0px'})),
                 dbc.CardBody(
                     html.Div(id='avg-traffic', className='big-number'))
                    
                ],className="card text-white bg-primary mb-3", style=avg_card_style)),
        
        dbc.Tooltip("Average, minimum, and maximum values of total traffic.", target="avg-traffic"),
       
    ]),
    
    html.H5("Trends in Public Transport Ridership Since 2020. A Journey from the Pandemic", style={'text-align': 'center'}),
    dbc.Row(
        dbc.Col(
            dbc.Card(dcc.Graph(id='mta-area'), className="card border-primary mb-3",
                     style=card_style)
        )),
    html.H5("Recovery in Percentages: Public Transport vs. Pre-Pandemic", style={'text-align': 'center'}),
    dbc.Row(
        dbc.Col(
            dbc.Card(dcc.Graph(id='mta-percentage'), className="card border-primary mb-3",
                     style=card_style)
        ))

    
])



def format_title(transportmodes, total_values):
    titles = []
    for mode, value in zip(transportmodes, total_values):
        if value >= 1e9:
            value_str = f"{value / 1e9:.1f}B"
        elif value >= 1e6:
            value_str = f"{value / 1e6:.1f}M"
        else:
            value_str = f"{value:.1f}"
        titles.append(f"{mode}: {value_str}")
    return " | ".join(titles)

def format_percentage_title(transportmodes, percentage_values):
    titles = []
    for mode, value in zip(transportmodes, percentage_values):
        titles.append(f"{mode}: {value:.1f}%")
    return " | ".join(titles)

def format_value(value):
    if value >= 1e6:
        return f"{value / 1e6:.1f}M"
    elif value >= 1e3:
        return f"{value / 1e3:.1f}K"
    else:
        return str(value)

@app.callback(
    [Output('avg-ridership', 'children'),
     Output('avg-scheduled-trips', 'children'),
     Output('avg-traffic', 'children'),
     Output("mta-area", "figure"),
     Output("mta-percentage", "figure")],
    [Input("mta-checklist", "value"),
     Input("date-radioitems", "value"),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date")]
)
def mta_plotter(transportmodes, date, start_date, end_date):
    
    filtered_df = mta_df[(mta_df['Date'] >= start_date) & (mta_df['Date'] <= end_date)]
    
    Transportation_ER = (filtered_df.set_index("Date")
                         .loc[:, ['Subways: Total Estimated Ridership',
                                  'Buses: Total Estimated Ridership',
                                  'LIRR: Total Estimated Ridership',
                                  'Metro-North: Total Estimated Ridership',
                                  'Staten Island Railway: Total Estimated Ridership',
                                  'Access-A-Ride: Total Scheduled Trips',
                                  'Bridges and Tunnels: Total Traffic']]
                         .rename(columns={'Subways: Total Estimated Ridership':'Subways',
                                          'Buses: Total Estimated Ridership':'Buses',
                                          'LIRR: Total Estimated Ridership':'Long Island Rails',
                                          'Metro-North: Total Estimated Ridership':'Metro-North',
                                          'Staten Island Railway: Total Estimated Ridership':'Staten Island Railway',
                                          'Access-A-Ride: Total Scheduled Trips':'Access-A-Rid',
                                          'Bridges and Tunnels: Total Traffic':'Bridges and Tunnels'})
                         .resample(date).sum())
    

    color_map = {
        'Subways': 'blue',
        'Buses': 'red',
        'Long Island Rails': 'green',
        'Metro-North': 'purple',
        'Staten Island Railway': 'orange',
        'Access-A-Rid': 'teal',
        'Bridges and Tunnels': 'brown'
    }
    
    total_values = [Transportation_ER[mode].sum() for mode in transportmodes] 
    title = format_title(transportmodes, total_values)
    max_mean_value = Transportation_ER[transportmodes].max().mean()


    fig = px.area(Transportation_ER,
                  x=Transportation_ER.index,
                  y=transportmodes,
                  color_discrete_map=color_map,
                  markers=True,
                  labels={'value': 'Totals', 'Date':'', 'variable': ''},
                  title=title,
                  template='plotly_white'
                 )
    
    fig.update_layout(
        legend=dict(
            title=None, orientation="h", y=0.96, yanchor="bottom", x=0.5, xanchor="center",
            font=dict(size=16)),
        
    
    )
    

    fig.add_annotation(x='2020-03-01', y=max_mean_value,
                       text="Start of Pandemic",
                       showarrow=True,
                       arrowhead=1)


    Percentage_ER = (filtered_df.set_index("Date")
                     .loc[:, ['Subways: % of Comparable Pre-Pandemic Day',
                              'Buses: % of Comparable Pre-Pandemic Day',
                              'LIRR: % of Comparable Pre-Pandemic Day',
                              'Metro-North: % of Comparable Pre-Pandemic Day',
                              'Staten Island Railway: % of Comparable Pre-Pandemic Day',
                              'Access-A-Ride: % of Comparable Pre-Pandemic Day',
                              'Bridges and Tunnels: % of Comparable Pre-Pandemic Day']]
                     .rename(columns={'Subways: % of Comparable Pre-Pandemic Day':'Subways',
                                      'Buses: % of Comparable Pre-Pandemic Day':'Buses',
                                      'LIRR: % of Comparable Pre-Pandemic Day':'Long Island Rails',
                                      'Metro-North: % of Comparable Pre-Pandemic Day':'Metro-North',
                                      'Staten Island Railway: % of Comparable Pre-Pandemic Day':'Staten Island Railway',
                                      'Access-A-Ride: % of Comparable Pre-Pandemic Day':'Access-A-Rid',
                                      'Bridges and Tunnels: % of Comparable Pre-Pandemic Day':'Bridges and Tunnels'})
                     .resample(date).mean())
    
    percentage_values = [Percentage_ER[mode].mean() for mode in transportmodes]
    percentage_title = format_percentage_title(transportmodes, percentage_values)

    fig2 = px.line(Percentage_ER,
                  x=Percentage_ER.index,
                  y=transportmodes,
                  color_discrete_map=color_map,
                  markers=True,
                  labels={'value': '% vs Pre-Pandemic Date', 'Date':'', 'variable': ''},
                  title=percentage_title,
                  template='plotly_white'
                 )
        
  
    fig2.update_layout(showlegend=False)
    fig2.add_annotation(x='2020-03-01', y=Percentage_ER[transportmodes].max().mean(),
                       text="Start of Pandemic",
                       showarrow=True,
                       arrowhead=1)
    

    
# Define the columns to process
    columns = [
        'Total Estimated Ridership',
        'Access-A-Ride: Total Scheduled Trips',
        'Bridges and Tunnels: Total Traffic'
    ]
    
  


# Calculate averages, min, and max for each column using pandas
    stats = filtered_df[columns].agg(['mean', 'min', 'max']).astype('int')



# Format the statistics
    formatted_stats = {col: {stat: format_value(stats.loc[stat, col]) for stat in stats.index} for col in columns}

    # Return the formatted values
    return ( f"avg: {formatted_stats['Total Estimated Ridership']['mean']}, min: {formatted_stats['Total Estimated Ridership']['min']}, max: {formatted_stats['Total Estimated Ridership']['max']}", f"avg: {formatted_stats['Access-A-Ride: Total Scheduled Trips']['mean']}, min: {formatted_stats['Access-A-Ride: Total Scheduled Trips']['min']}, max: {formatted_stats['Access-A-Ride: Total Scheduled Trips']['max']}", f"avg: {formatted_stats['Bridges and Tunnels: Total Traffic']['mean']}, min: {formatted_stats['Bridges and Tunnels: Total Traffic']['min']}, max: {formatted_stats['Bridges and Tunnels: Total Traffic']['max']}", fig, fig2 )



    





if __name__ == '__main__':
    app.run(debug=True,port=8063)


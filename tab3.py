import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dateutil
import plotly.graph_objs as go
import pandas as pd
import json
from dash.dependencies import Input, Output
from app import app
##############################################################
#                                                            #
#             D  A  T  A     L  O  A  D  I  N  G             #
#                                                            #
##############################################################

df = pd.read_csv('cars.csv', parse_dates=True)
df['name'] = df.apply(lambda row: row.model.split(" ")[0], 1)
df_grouped = df.groupby('name').mean()

cylinders = [{'label': str(i)+' Cylinders', 'value': i} for i in sorted(df.cyl.unique())]
cylinders.insert(0,{'label':'All Cylinders', 'value':'All'})

regions = [{'label': 'Region '+str(i), 'value': i} for i in sorted(df.region.unique())]
regions.insert(0,{'label':'All Regions', 'value':'All'})

region_colors = ['blue', 'red', 'green']
color_blocks = '#90a4ae'


column_dict = [{'label':'Miles per Gallon', 'value':'mpg'}, 
               {'label':'Displacement', 'value':'disp'}, 
               {'label':'Cylinders', 'value':'cyl'}, 
               {'label':'Horsepower', 'value':'hp'}, 
               {'label':'Weight', 'value':'weight'}, 
               {'label':'Acceleration', 'value':'acc'}, 
               {'label':'Year', 'value':'year'},
               {'label':'Region', 'value':'region'}, 
               {'label':'Model', 'value':'model'}, 
               {'label':'Name', 'value':'name'}]

column_lookup = {'Miles per Gallon':'mpg', 
               'Displacement':'disp', 
               'Cylinders':'cyl', 
               'Horsepower':'hp', 
               'Weight':'weight', 
               'Acceleration':'acc', 
               'Year':'year',
               'Region':'region', 
               'Model':'model', 
               'Name':'name'}
column_lookup = {v: k for k, v in column_lookup.items()}

##############################################################
#                                                            #
#                   L  A  Y  O  U  T                         #
#                                                            #
##############################################################


layout = html.Div(style={'backgroundColor': '#F2F2F2', 
                         'border-bottom-left-radius': '25px',
                        'border-bottom-right-radius': '25px',
                        'height':'120%','padding-bottom':50},children=[

    # Lower exploration filter
    html.Div(className='exploration-container', children=[
        html.Div('Choose x-axis', style={'font-weight':'bold', 'marginLeft':150}),
        dcc.Dropdown(className='dropdown-style',
            id='T3 x_axis',
            options=column_dict,
            value='mpg',
            clearable=False,
                 style={"height": "20",
                   "background": "white",
                   "color": "black"}
            ),
        ]
    ),   
    html.Div(className='exploration-container',children=[
        html.Div('Choose y-axis', style={'font-weight':'bold', 'marginLeft':150}),
        dcc.Dropdown(
            id='T3 y_axis',
            options=column_dict,
            value='hp',
            clearable=False,
                 style={"height": "20",
                   "background": "white",
                   "color": "black"}
            ),
        ]
    ),  
    
    
    # Graph
    html.Div(className='viz-container',children=[
        dcc.Graph(className='viz-block',
            id='T3 exploration',
            config={'displayModeBar': False}
        )
        ]),
    html.Div(className='viz-container',children=[
            dcc.Graph(className='viz-block',
                id='T3 exploration2',
                config={'displayModeBar': False}
            )
            ]),

])


##############################################################
#                                                            #
#            I  N  T  E  R  A  C  T  I  O  N  S              #
#                                                            #
##############################################################

@app.callback(
    dash.dependencies.Output('T3 exploration', 'figure'),
    [
        dash.dependencies.Input('T3 x_axis', 'value'),
        dash.dependencies.Input('T3 y_axis', 'value'),
    ])
def update_exploration(x_axis, y_axis):
    
    sub_df = df_grouped.copy()
    sub_df = sub_df.reset_index()
    
    print(x_axis)
    
    return {
        'data': [
            go.Scatter(
                x=sub_df[x_axis],
                y=sub_df[y_axis],
                text=sub_df.reset_index().name.values,
                mode='markers',
                opacity=0.9,
                marker={
                    'size': 11,
                    'color': '#89AEF6',
                },
            )
        ],
        'layout': go.Layout(
            xaxis=dict(
                showgrid=False,
                showline=True,
                zeroline=True,
                title= column_lookup[x_axis],
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                title=column_lookup[y_axis],
            ),
            margin={'l': 50, 'b': 50, 't': 60, 'r': 0},
            height=365,
            autosize=False,
            showlegend=False,            
            hovermode='closest',
            title='<b>All Major Models</b><br>{} vs. {}'.format(column_lookup[x_axis], column_lookup[y_axis]),
        )
    }


@app.callback(
    dash.dependencies.Output('T3 exploration2', 'figure'),
    [
        dash.dependencies.Input('T3 x_axis', 'value'),
        dash.dependencies.Input('T3 y_axis', 'value'),
        dash.dependencies.Input('T3 exploration', 'hoverData'),

    ])
def update_exploration_new(x_axis, y_axis, hover):
    if hover:
        name = hover['points'][0]['text']
        highlight = df.loc[df.name == name, :].copy()
        lowlight = df.loc[df.name != name, :].copy()
        colors = ['#89AEF6', 'red']
    else: 
        highlight = df
        lowlight = df
        name = 'All Models'
        colors = ['#89AEF6', '#89AEF6']
  
    return {
        'data': [
            go.Scatter(
                x=lowlight[x_axis],
                y=lowlight[y_axis],
                text=lowlight.model,
                mode='markers',
                opacity=1,
                marker={
                    'size': 9,
                    'color': colors[0],
                }) ,
            go.Scatter(
                x=highlight[x_axis],
                y=highlight[y_axis],
                text=highlight.model,
                mode='markers',
                opacity=1,
                marker={
                    'size': 9,
                    'color': colors[1],
                }) 
        ],
        'layout': go.Layout(
            xaxis=dict(
                showgrid=False,
                showline=True,
                zeroline=True,
                title= column_lookup[x_axis],
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                title=column_lookup[y_axis],
            ),
            margin={'l': 50, 'b': 50, 't': 60, 'r': 0},
            height= 365,
            showlegend=False,            
            hovermode='closest',
            title='<b>{}</b><br>{} vs. {}'.format(name, column_lookup[x_axis], column_lookup[y_axis]),
        )
    }

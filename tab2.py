
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

cylinders = [{'label': str(i)+' Cylinders', 'value': i} for i in sorted(df.cyl.unique())]
cylinders.insert(0,{'label':'All Cylinders', 'value':'All'})

regions = [{'label': 'Region '+str(i), 'value': i} for i in sorted(df.region.unique())]
regions.insert(0,{'label':'All Regions', 'value':'All'})

region_colors = ['#CE0106', '#F6BF00', '#5DC1D0']
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
    
    # Top filter
    html.Div(className='filter-container', children=[
        html.Div('Choose Filter(s)',style={'font-weight':'bold', 'marginLeft':300,
                                       'font-size':20, 'padding-top':10}),
    html.Div(children=[
        
        # Cylinders
        dcc.Dropdown(
            id='T2 cylinders',
            options=cylinders,
            value='All',
            clearable=False,
                 style={"height": "20",
                   "background": "white",
                   "color": "black"}
            ),
        ], style={'width': '20%', 'marginLeft': 160, 'display': 'inline-block',
                 'marginTop':20}
    ),
        
        # Regions
        html.Div(children=[
            dcc.Checklist(
                id='T2 Region 1',
                options=[
                    {'label': 'USA', 'value': 1},
                ],
                values=[1],
            ),
            ], style={'width': '12%',
                      "color": region_colors[0],'display': 'inline-block',
                     'font-weight':'bold','marginLeft':50, 'marginTop':20}
        ), 
        html.Div(children=[
            dcc.Checklist(
                id='T2 Region 2',
                options=[
                    {'label': 'Europe', 'value': 2},
                ],
                values=[2]
            ),
            ], style={'width': '12%', 'marginLeft':10,
                      "color": region_colors[1],
                      'font-weight':'bold','display': 'inline-block'}
        ), 
        html.Div(children=[
            dcc.Checklist(
                id='T2 Region 3',
                options=[
                    {'label': 'Asia', 'value': 3},
                ],
                values=[3]
            ),
            ], style={'width': '12%',  'marginLeft':10,
                     "color": region_colors[2],
                     'font-weight':'bold','display': 'inline-block'}
        ),

    
    # Slider
    html.Div(children=[dcc.Slider(
        id='T2 year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].max(),
        marks={str(year): '19'+str(year) for year in df['year'].unique()}
    )], style={'width': '70%', 'marginLeft': 100, 'display': 'inline-block', 
              'marginTop':35}),   ]), 


    # Lower exploration filter
    html.Div(className='exploration-container', children=[
        html.Div('Choose x-axis', style={'font-weight':'bold', 'marginLeft':150,'marginTop':5}),
        dcc.Dropdown(className='dropdown-style',
            id='T2 x_axis',
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
        html.Div('Choose y-axis', style={'font-weight':'bold', 'marginLeft':150,'marginTop':5}),
        dcc.Dropdown(
            id='T2 y_axis',
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
    html.Div(className='viz-container-one-column', children=[
        dcc.Graph(className='viz-block-one-column',
            id='T2 exploration',
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
    dash.dependencies.Output('T2 exploration', 'figure'),
    [
        dash.dependencies.Input('T2 cylinders', 'value'),
        dash.dependencies.Input('T2 year-slider', 'value'),
        dash.dependencies.Input('T2 Region 1', 'values'),
        dash.dependencies.Input('T2 Region 2', 'values'),
        dash.dependencies.Input('T2 Region 3', 'values'),
        dash.dependencies.Input('T2 x_axis', 'value'),
        dash.dependencies.Input('T2 y_axis', 'value'),
    ])
def update_exploration(cylinders, year, region_1, region_2, region_3, x_axis, y_axis):
    regions = region_1+region_2+region_3
    sub_df = df[(df.year<=year)&(df.region.isin(regions))]

    if (type(cylinders) != str):
        sub_df = sub_df[(sub_df['cyl'] == cylinders)]

    return {
        'data': [
            go.Scatter(
                x=sub_df[sub_df.region==region_index][x_axis],
                y=sub_df[sub_df.region==region_index][y_axis],
                text=sub_df.model,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'color': color,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name='Region '+str(region_index),
            ) for region_index,color in zip([1, 2, 3], region_colors)
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
            margin={'l': 50, 'b': 50, 't': 30, 'r': 30},
            height= 450,
            width=800,
            showlegend=False,            
            hovermode='closest',
            title='<b>{} vs. {}'.format(column_lookup[x_axis], column_lookup[y_axis]),

            
            
        )
    }

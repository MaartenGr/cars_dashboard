
#### To Do:
# https://plot.ly/python/images/


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

def create_relayout_data(x_name, y_name, relayoutData, df):
    if relayoutData:
        if 'yaxis.range[1]' in relayoutData.keys():
            y_max = relayoutData['yaxis.range[1]']
            y_min = relayoutData["yaxis.range[0]"]
            x_max = relayoutData["xaxis.range[1]"]
            x_min = relayoutData["xaxis.range[0]"]

            sub_df = df[df[x_name].between(x_min, x_max)].copy()
            sub_df = sub_df[sub_df[y_name].between(y_min, y_max)]
            
            return sub_df
    return df

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

region_colors = ['#9575cd', '#64b5f6', '#e57373']
region_colors = ['#CE0106', '#F6BF00', '#5DC1D0']


color_blocks = '#90a4ae'

color_title = "#4db6ac"
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

dependencies_dict = {'cylinder':'value', 'year-slider':'value',
                    'Region 1':'values','Region 2':'values',
                    'Region 3':'values', 'hp_disp':'relayoutData',
                    'weight_mpg':'relayoutData', 'weight_acc':'relayoutData'}

margins = {'l': 50, 'b': 50, 't': 60, 'r': 0}


def create_dependencies_list(names, dependencies_dict):
    return [Input(name, dependencies_dict[name]) for name in names]

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
            id='cylinders',
            options=cylinders,
            value='All',
            clearable=False,
                 style={"height": "20",
                   "background": "white",
                   "color": "black"}
            ),
        ], style={'width': '20%', 'marginLeft': 160, 'display': 'inline-block',
                 'marginTop':20, 'font-family': 'Arial, Helvetica, sans-serif'}
    ),
        
        # Regions
        html.Div(children=[
            dcc.Checklist(
                id='Region 1',
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
                id='Region 2',
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
                id='Region 3',
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
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].max(),
        marks={str(year): '19'+str(year) for year in df['year'].unique()}
    )], style={'width': '70%', 'marginLeft': 100, 'display': 'inline-block', 
              'marginTop':35}),   ]), 

    # GRAPHS
    html.Div(className='viz-container', children=[
        dcc.Graph(className='viz-block',
            id='weight_acc',
            config={'displayModeBar': False}
        )
        ]),
    
     html.Div(className='viz-container', children=[
        dcc.Graph(className='viz-block',
            id='hp_disp',
            config={'displayModeBar': False}
        )
        ]),
    html.Div(className='viz-container',children=[
        dcc.Graph(className='viz-block',
            id='disp',
            config={'displayModeBar': False}
        )
        ]),
     html.Div(className='viz-container',children=[
        dcc.Graph(className='viz-block',
            id='usd-pledged-vs-date2',
            config={'displayModeBar': False}
        )
        ]),
     html.Div(className='viz-container',children=[
        dcc.Graph(className='viz-block',
            id='weight_mpg',
            config={'displayModeBar': False}
        )
        ]),
     html.Div(className='viz-container',children=[
        dcc.Graph(className='viz-block',
            id='horsepower',
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
    dash.dependencies.Output('weight_acc', 'figure'),
    [
        dash.dependencies.Input('cylinders', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        dash.dependencies.Input('Region 1', 'values'),
        dash.dependencies.Input('Region 2', 'values'),
        dash.dependencies.Input('Region 3', 'values'),
        Input('hp_disp', 'relayoutData'),
        Input('weight_mpg', 'relayoutData'),
        Input('weight_acc', 'relayoutData'),
    ])
def update_scatterplot_weight_acc(cylinders, year, region_1, region_2, region_3,
                                 relayout_hp_disp, relayout_weight_mpg, relayoutData):
    regions = region_1+region_2+region_3
    sub_df = df[(df.year<=year)&(df.region.isin(regions))]
    range_x = [0, 5500]
    range_y = [-1, 30]
    
    if (type(cylinders) != str):
        sub_df = sub_df[(sub_df['cyl'] == cylinders)]

    if relayoutData:
        sub_df = create_relayout_data('weight', 'acc', relayoutData, sub_df)     
        range_x = [sub_df.weight.min()*0.9, 
                  sub_df.weight.max()*1.1]
        range_y = [sub_df.acc.min()*0.9, 
                  sub_df.acc.max()*1.1]
    if relayout_hp_disp:
        sub_df = create_relayout_data('hp', 'disp', relayout_hp_disp, sub_df)
    if relayout_weight_mpg:
        sub_df = create_relayout_data('weight', 'mpg', relayout_weight_mpg, sub_df)
  
    return {
        'data': [
            go.Scatter(
                x=sub_df[sub_df.region==region_index].weight,
                y=sub_df[sub_df.region==region_index].acc,
                text=sub_df.model,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 8,
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
                title= 'Weight',
                range=range_x
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                title='Acceleration',
                range=range_y
            ),
            margin=margins,
            height= 370,
            showlegend=False,            
            hovermode='closest',
            title='<b>Weight vs. Acceleration',
        )
    }

@app.callback(
    dash.dependencies.Output('horsepower', 'figure'),
    [
        dash.dependencies.Input('cylinders', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        Input('weight_acc', 'relayoutData'),
        dash.dependencies.Input('Region 1', 'values'),
        dash.dependencies.Input('Region 2', 'values'),
        dash.dependencies.Input('Region 3', 'values'),
        Input('hp_disp', 'relayoutData'),
        Input('weight_mpg', 'relayoutData'),


    ])
def update_histogram_horsepower(cylinders, year, relayoutData, 
                                region_1, region_2, region_3, relayout_hp_disp,
                               relayout_weight_mpg):
    regions = region_1+region_2+region_3
    sub_df = df[(df.year<=year)&(df.region.isin(regions))]

    if (type(cylinders) != str):
        sub_df = sub_df[(sub_df['cyl'] == cylinders)]
        
    if relayoutData:
        sub_df = create_relayout_data('weight', 'acc', relayoutData, sub_df)        
    if relayout_hp_disp:
        sub_df = create_relayout_data('hp', 'disp', relayout_hp_disp, sub_df)
    if relayout_weight_mpg:
        sub_df = create_relayout_data('weight', 'mpg', relayout_weight_mpg, sub_df)

    return {       
        'data': [
            go.Histogram(x=sub_df.hp,marker=dict(color=color_title))
        ],
        'layout': go.Layout(
            xaxis=dict(
                showgrid=False,
                showline=True,
                zeroline=True,
                title= '',
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                title='',
            ),
            margin=margins,
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            height= 370,
            title='<b>Horsepower Distribution',

        )
    }

@app.callback(
    dash.dependencies.Output('usd-pledged-vs-date2', 'figure'),
    [
        dash.dependencies.Input('cylinders', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        Input('weight_acc', 'relayoutData'),
        dash.dependencies.Input('Region 1', 'values'),
        dash.dependencies.Input('Region 2', 'values'),
        dash.dependencies.Input('Region 3', 'values'),
        Input('hp_disp', 'relayoutData'),
        Input('weight_mpg', 'relayoutData'),


    ])
def update_histogram_models(cylinders, year, relayoutData, region_1, region_2, region_3,
                           relayout_hp_disp, relayout_weight_mpg):
    regions = region_1+region_2+region_3
    sub_df = df[(df.year<=year)&(df.region.isin(regions))]

    if (type(cylinders) != str):
        sub_df = sub_df[(sub_df['cyl'] == cylinders)]

    if relayoutData:
        sub_df = create_relayout_data('weight', 'acc', relayoutData, sub_df)        
    if relayout_hp_disp:
        sub_df = create_relayout_data('hp', 'disp', relayout_hp_disp, sub_df)
    if relayout_weight_mpg:
        sub_df = create_relayout_data('weight', 'mpg', relayout_weight_mpg, sub_df)
  
    y = sub_df.groupby('name').count().sort_values('mpg', ascending=False).mpg[:10].index
    x = sub_df.groupby('name').count().sort_values('mpg', ascending=False).mpg[:10].values

    return {       
        'data': [
            go.Bar(
            x=x,
            y=y,
            orientation = 'h',
            marker=dict(color=color_title))]
        ,
        'layout': go.Layout(
            xaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                title= '',
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                title='',
            ),
            margin={'l': 80, 'b': 30, 't': 30, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            height= 380,
            title='<b>Most Common Models',
        )
    }

@app.callback(
    dash.dependencies.Output('hp_disp', 'figure'),
    [
        dash.dependencies.Input('cylinders', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        Input('weight_acc', 'relayoutData'),
        dash.dependencies.Input('Region 1', 'values'),
        dash.dependencies.Input('Region 2', 'values'),
        dash.dependencies.Input('Region 3', 'values'),
        Input('weight_mpg', 'relayoutData'),
        Input('hp_disp', 'relayoutData'),


    ])
def update_scatterplot_hp_acc(cylinders, year,relayoutData, region_1, region_2, region_3,
                             relayout_weight_mpg, relayout_hp_disp):
    regions = region_1+region_2+region_3
    sub_df = df[(df.year<=year)&(df.region.isin(regions))]
    
    range_x = [0, 275]
    range_y = [0, 500]

    if (type(cylinders) != str):
        sub_df = sub_df[(sub_df['cyl'] == cylinders)]

    if relayoutData:
        sub_df = create_relayout_data('weight', 'acc', relayoutData, sub_df)        
    if relayout_hp_disp:
        sub_df = create_relayout_data('hp', 'disp', relayout_hp_disp, sub_df)
        range_x = [sub_df.hp.min()*0.9, 
                  sub_df.hp.max()*1.1]
        range_y = [sub_df.disp.min()*0.9, 
                  sub_df.disp.max()*1.1]
    if relayout_weight_mpg:
        sub_df = create_relayout_data('weight', 'mpg', relayout_weight_mpg, sub_df)

    return {
        'data': [
            go.Scatter(
                x=sub_df[sub_df.region==region_index].hp,
                y=sub_df[sub_df.region==region_index].disp,
                text=sub_df.model,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 8,
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
                title= 'Horsepower',
                range=range_x
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                title='Displacement',
                range=range_y
            ),
            margin=margins,
            height= 370,
            showlegend=False,            
            hovermode='closest',
            title='<b>Horsepower vs. Displacement',
        )
    }

@app.callback(
    dash.dependencies.Output('disp', 'figure'),
    [
        dash.dependencies.Input('cylinders', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        Input('weight_acc', 'relayoutData'),
        dash.dependencies.Input('Region 1', 'values'),
        dash.dependencies.Input('Region 2', 'values'),
        dash.dependencies.Input('Region 3', 'values'),
        Input('hp_disp', 'relayoutData'),
        Input('weight_mpg', 'relayoutData'),


    ])
def update_histogram_disp(cylinders, year, relayoutData, region_1, region_2, region_3,
                         relayout_hp_disp, relayout_weight_mpg):
    regions = region_1+region_2+region_3
    sub_df = df[(df.year<=year)&(df.region.isin(regions))]

    if (type(cylinders) != str):
        sub_df = sub_df[(sub_df['cyl'] == cylinders)]

    if relayoutData:
        sub_df = create_relayout_data('weight', 'acc', relayoutData, sub_df)        
    if relayout_hp_disp:
        sub_df = create_relayout_data('hp', 'disp', relayout_hp_disp, sub_df)
    if relayout_weight_mpg:
        sub_df = create_relayout_data('weight', 'mpg', relayout_weight_mpg, sub_df)

    return {       
        'data': [
            go.Histogram(x=sub_df.disp,marker=dict(color=color_title)
)
        ],
        'layout': go.Layout(
            xaxis=dict(
                showgrid=False,
                showline=True,
                zeroline=True,
                title= '',
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                title='',
            ),
            margin=margins,
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            height= 380,
            title='<b>Displacement Distribution',
        )
    }

@app.callback(
    dash.dependencies.Output('weight_mpg', 'figure'),
    [
        dash.dependencies.Input('cylinders', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        Input('weight_acc', 'relayoutData'),
        dash.dependencies.Input('Region 1', 'values'),
        dash.dependencies.Input('Region 2', 'values'),
        dash.dependencies.Input('Region 3', 'values'),
        Input('hp_disp', 'relayoutData'),
        Input('weight_mpg', 'relayoutData'),

    ])
def update_scatterplot_weight_mpg(cylinders, year,relayoutData, region_1, region_2, region_3,
                                 relayout_hp_disp,relayout_weight_mpg):
    regions = region_1+region_2+region_3
    sub_df = df[(df.year<=year)&(df.region.isin(regions))]
    range_x = [100, 5500]
    range_y = [0, 50]

    if (type(cylinders) != str):
        sub_df = sub_df[(sub_df['cyl'] == cylinders)]

    if relayoutData:
        sub_df = create_relayout_data('weight', 'acc', relayoutData, sub_df)        
    if relayout_hp_disp:
        sub_df = create_relayout_data('hp', 'disp', relayout_hp_disp, sub_df)
    if relayout_weight_mpg:
        sub_df = create_relayout_data('weight', 'mpg', relayout_weight_mpg, sub_df)
        range_x = [sub_df.weight.min()*0.9, 
                  sub_df.weight.max()*1.1]
        range_y = [sub_df.mpg.min()*0.9, 
                  sub_df.mpg.max()*1.1]


    return {
        'data': [
            go.Scatter(
                x=sub_df[sub_df.region==region_index].weight,
                y=sub_df[sub_df.region==region_index].mpg,
                text=sub_df.model,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 8,
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
                title= 'Weight',
                range=range_x,
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                title='Miles/Gallon',
                range=range_y,
            ),
            margin=margins,
            height= 370,
            showlegend=False,            
            hovermode='closest',
            title='<b>Weight vs. Miles/Gallon',
        )
    }
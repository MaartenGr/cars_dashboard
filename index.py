import dash
import dash_html_components as html
import dash_core_components as dcc
import tab1
import tab2
import tab3
from app import app
from dash.dependencies import Input, Output
img = 'https://hennydonovanmotif.co.uk/wp-content/uploads/2016/10/circle-stencil2.jpg'
img = 'https://i.imgur.com/FaufZBM.png'
img = 'https://i.imgur.com/LoutMRR.png'

# img = 'https://i.imgur.com/0cEyIFb.png'
# img = 'http://www.allwhitebackground.com/images/2/2270.jpg'
# img = 'https://www.wexphotovideo.com/globalassets/product-images/1538000/1538846-2.jpg'
# img = 'https://images.pexels.com/photos/988872/pexels-photo-988872.jpeg?cs=srgb&dl=abstract-attractive-backdrop-988872.jpg&fm=jpg'

app.layout = html.Div(html.Div([
    # Tabs
    dcc.Tabs(parent_className = 'custom-tabs',
             className = 'custom-tabs-container',
             style={'marginBottom':0,'marginTop':0, 'width':'82%', 'marginLeft':80,
                   'height':'10%',"background": "white"},
             id="tabs", value='tab-1', children=[
        dcc.Tab(label='Dashboard', value='tab-1', 
                className='custom-tab',
                selected_className='custom-tab--selected'),
        dcc.Tab(label='Exploration', value='tab-2', 
                className='custom-tab',
                selected_className='custom-tab--selected'),
        dcc.Tab(label='Hover', value='tab-3', 
                className='custom-tab',
                selected_className='custom-tab--selected'),
    ], colors={
        "background": "white"
    }
),
    html.Div(id='tabs-content', style={'border-radius': '25px', "background": "white"})
], style={'width':'70%','height':'150%',
         'marginLeft':190, 
         'background':'white',
         'display':'block',
         '-moz-box-shadow': '0px 0px 5px #bfbfbf',
         '-webkit-box-shadow': '0px 0px 5px #bfbfbf',
         'box-shadow': '0px 0px 5px #bfbfbf',
         'border-radius': '25px'}),
                      style = {'background':"url('{}')".format(img), 'padding-top':'100px', 'padding-bottom':'60px', 'display':'block'
                               }
                     )
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    elif tab == 'tab-2':
        return tab2.layout
    elif tab == 'tab-3':
        return tab3.layout


if __name__ == '__main__':
    app.run_server(debug=True)
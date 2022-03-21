import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import base64
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

app = dash.Dash('dashboard_app',
                title='Demand Forecasting',
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read in global data

infos  = pd.read_csv('data/infos.csv',  sep = '|')
items  = pd.read_csv('data/items.csv',  sep = '|')
#orders = pd.read_csv('data/orders.csv', sep = '|')
orders_day = pd.read_csv('data/orders_day.csv')
orders_month = pd.read_csv('data/orders_month.csv')
agg_orders_day = pd.read_csv('data/agg_orders_day.csv')
agg_orders_month = pd.read_csv('data/agg_orders_month.csv')
result = pd.read_csv('data/result.csv')

items = pd.merge(infos, items, on = 'itemID', how = 'left')
del infos

# orders['time'] = pd.to_datetime(orders['time'].astype('str'))
# orders['day_of_year'] = orders['time'].dt.dayofyear
# orders['month'] = orders['time'].dt.strftime('%m-%Y')


# agg_order_daily = orders.groupby(['day_of_year'])['order'].agg('sum').reset_index()
# agg_order_monthly = orders.groupby(['month'])['order'].agg('sum').reset_index()

mean_price_daily = agg_orders_day.groupby(['itemID'])['salesPrice'].agg('mean').reset_index()
# mean_price_monthly = orders.groupby(['month'])['salesPrice'].agg('mean').reset_index()

item_list = items["itemID"].unique()
item_list.sort()

manuf_list = items['manufacturer'].unique()
manuf_list.sort()



# Setup collapse button

collapse_button = dbc.Row(
    dbc.Button('Help', id='top-level-collapse-button', color='primary'),
    no_gutters=True,
    className='ml-auto flex-nowrap mt-5 mt-md-0',
    align='center'
)

collapse = dbc.Collapse(
    [
        dbc.Card(dbc.CardBody(
            [
                html.P('Welcome to the demand forecasting dashboard. This dashboard is created to help optimize '
                       'inventory and reduce cost, improve profit and faster drlivery '
                       'organizations understand why supporting mental health is essential.'),
                html.H5('Tabs and dashboards'),
                html.P('There are 2 clickable tabs in the app. The dashboard in Basic EDA tab contains overall '
                       'summaries of orders, prices and customer rating. The dashboard in Forecast tab contains '
                       'comparision of predictions with actual orders.'),
                html.H5('Interactive components'),
                html.P('All plots contains interactive components like tooltips that can reveal more information when '
                       'you hover your mouse on the figures. '),
                html.Hr(),
                html.P('This message can be collapsed/hidden by clicking the Help button at the top right corner.')
            ]
        )),
        html.Br()
    ],
    id='dashboard_description')


@app.callback(
    Output('dashboard_description', 'is_open'),
    [Input('top-level-collapse-button', 'n_clicks')],
    [State('dashboard_description', 'is_open')],
)
def toggle_collapse(n, is_open):
    """
    Simple callback that will toggle the collapse
    :param n: The initial state of n_clicks
    :param is_open: The initial state of is_open
    :return: The result state of is_open after it is toggled
    """
    if n:
        return not is_open
    return is_open


# Setup Graph
# Colours
color_1 = "#003399"
color_2 = "#00ffff"
color_3 = "#002277"
color_b = "#F8F8FF"


# daily

fig_day = go.Figure()

fig_day.add_trace(go.Bar(
            x=orders_day['day_of_year'],
            y=orders_day['order'],
            marker={"color": color_1},
            name="Total Orders"
        ))

fig_day.add_trace(go.Scatter(
                x=orders_day['day_of_year'],
                y=orders_day['salesPrice'],
                hoverinfo="y",
                line={
                    "color": "#e41f23",
                    "dash": "dot",
                    "width": 2,
                },
                marker={
                    "maxdisplayed": 0,
                    "opacity": 0,
                },
                name="Avg. Sales Price",
            ))
    

fig_day.update_layout(
            autosize=False,
            plot_bgcolor="rgb(255, 255, 255, 0)",
            bargap=0.5,
            dragmode="pan",
            height=390,
            width=1050,
            hovermode="closest",
            legend={
                "x": 0.1,
                "y": -0.08,
                "bgcolor": "rgb(255, 255, 255, 0)",
                "borderwidth": 0,
                "font": {"size": 12},
                "orientation": "h",
            },
            margin={
                "r": 0,
                "t": 50,
                "b": 40,
                "l": 0,
                "pad": 0,
            },
            showlegend=True,
            title="Aggregate Orders - Daily ",
            title_x=0.5,
            titlefont={"size": 20},
            xaxis={
                "autorange": False,
                "nticks": 50,
                "range": [-0.5, 60.5],
                "tickangle": -90,
                "showgrid": False,
                "tickfont": {"size": 10},
                "tickmode": "linear",
                "ticks": "",
                "title": "Day of Year",
                "type": "category",
            },
            yaxis={
                "autorange": True,
                "linecolor": "rgb(176, 177, 178)",
                "nticks": 10,
                "range": [
                    -1283.8982436029166,
                    3012.5614936594166,
                ],
                "showgrid": True,
                "gridcolor": "rgb(220, 220, 220)",
                "showline": True,
                "tickfont": {"size": 12},
                "ticks": "outside",
                "title": "",
                "type": "linear",
                "zeroline": True,
                "zerolinecolor": "rgb(176, 177, 178)",
            },
        )

# monthly

fig_month = go.Figure()

fig_month.add_trace(go.Bar(
            x=["Jan-18", "Feb-18", "Mar-18", "Apr-18", "May-18", "Jun-18"],
            y=orders_month['order'],
            marker={"color": color_1}
        ))

fig_month.add_trace(go.Scatter(
                x=["Jan-18", "Feb-18", "Mar-18", "Apr-18", "May-18", "Jun-18"],
                    y=orders_month['salesPrice'],
                    hoverinfo="y",
                    line={
                        "color": "#e41f23",
                        "dash": "dot",
                        "width": 2,
                    },
                    marker={
                        "maxdisplayed": 0,
                        "opacity": 0,
                    },
                    name="Avg. Sales Price",
            ))

fig_month.update_layout(
            autosize=False,
            plot_bgcolor="rgb(255, 255, 255, 0)",
            bargap=0.3,
            dragmode="pan",
            height=400,
            width=360,
            hovermode="closest",
            margin={
                "r": 10,
                "t": 50,
                "b": 40,
                "l": 0,
                "pad": 0,
            },
            showlegend=False,
            title="Monthly",
            title_x=0.5,
            titlefont={"size": 20},
            xaxis={
                "autorange": False,
                "nticks": 10,
                "range": [-0.5, 6],
                "tickangle": -90,
                "showgrid": False,
                "tickfont": {"size": 10},
                "tickmode": "linear",
                "ticks": "",
                "title": "",
                "type": "category",
            },
            yaxis={
                "autorange": True,
                "linecolor": "rgb(176, 177, 178)",
                "nticks": 10,
                "range": [
                    -1283.8982436029166,
                    3012.5614936594166,
                ],
                "showgrid": True,
                "gridcolor": "rgb(220, 220, 220)",
                "showline": True,
                "tickfont": {"size": 12},
                "ticks": "outside",
                "title": "",
                "type": "linear",
                "zeroline": True,
                "zerolinecolor": "rgb(176, 177, 178)",
            },
        )

eda_1 =  dbc.Col([
                dbc.Row(children = [
                    dbc.Col(
                        html.Div([
                        dcc.Graph(figure=fig_day),
                        ]),width=9),
                    dbc.Col(
                        html.Div([
                        dcc.Graph(figure=fig_month),
                    ]),width=3)
                ]),
            ])


eda_2 = dbc.Col([
                dbc.Row(
                    dbc.Col([
                    dbc.Label('Item Id.'),
                    dcc.Dropdown(
                    id='item-id-dropdown',
                    value=item_list[0],
                    multi=False,
                    options=[{'label': col, 'value': col} for col in item_list]),
                    dbc.FormText('Select an item to view orders')
                      ], width=3)),
                html.Br(),
                dbc.Row(
                    dbc.Col(
                        [
                            dbc.CardDeck(
                                [
                                    dbc.Card(
                                        dbc.CardBody([
                                        html.P("Avg. Sales Price", className="card-title"),
                                        html.H4(id="sales-price", className="card-text"),
                                    ]),
                                    color="primary",
                                    outline=True,
                                ),
                                    dbc.Card(
                                        dbc.CardBody([
                                        html.P("Promotion Price", className="card-title"),
                                        html.H4(id="promotion-price", className="card-text"),
                                    ]),
                                    color="primary",
                                    outline=True,
                                ),
                                   dbc.Card(
                                        dbc.CardBody([
                                        html.P("Retail Price", className="card-title"),
                                        html.H4(id="retail-price", className="card-text"),
                                    ]),
                                    color="primary",
                                    outline=True,
                                ),
                                    dbc.Card(
                                        dbc.CardBody([
                                        html.P("Customer Rating", className="card-title"),
                                        html.H4(id="customer-rating", className="card-text"),
                                    ]),
                                    color="primary",
                                    outline=True,
                                ),
                                    dbc.Card(
                                        dbc.CardBody([
                                        html.P("Manufacturer", className="card-title"),
                                        html.H4(id="manufacturer", className="card-text"),
                                    ]),
                                    color="primary",
                                    outline=True,
                                ),
                                ])
                            ])
                        ),
                html.Br(),
                dbc.Row(children = [
                    dbc.Col(
                        html.Div([
                        dcc.Graph(id='item-daily-chart'),
                        ]),width=9),
                    dbc.Col(
                        html.Div([
                        dcc.Graph(id='item-month-chart'),
                    ]),width=3)
                ]),
            ])

eda_3 =  dbc.Col([
                dbc.Row(children=[
                    dbc.Col([
                    dbc.Label('Price Type'),
                    dcc.Dropdown(
                    id='price-dropdown',
                    options=[
                        {'label': 'Simulation', 'value': 'Simulation'},
                        {'label': 'Retail', 'value': 'Retail'}
                    ],
                    multi=True,
                    value=['Simulation', 'Retail']),
                    dbc.FormText('Select a price type to view histogram')
                      ], width=4),
                    dbc.Col([
                    dbc.Label('Manufacturer Id.'),
                    dcc.Dropdown(
                    id='manuf-id-dropdown',
                    value=manuf_list[0],
                    multi=False,
                    options=[{'label': col, 'value': col} for col in manuf_list]),
                    dbc.FormText('Select manufacturer to view ratings')
                    ], width=4, style={"margin-left": "270px"}),      
                ]),
                html.Br(),
                dbc.Row(children = [
                    dbc.Col(
                        html.Div([
                        dcc.Graph(id='price-chart'),
                        ]),width=6),
                    dbc.Col(
                        html.Div([
                        dcc.Graph(id='fig-rating'),
                    ]),width=6)
                ]),
            ])


eda_content = dbc.Card(
    dbc.CardBody([
        html.Br(),
        eda_1,
        html.Br(),
        eda_2,
        html.Br(),
        eda_3
    ]),color="primary", outline=True,
)

agg_forecast_fig = go.Figure()

agg_forecast_fig.add_trace(go.Bar(
                x=[i for i in range(145, 170)],
                y=result['Truth'],
                name='Actual',
                marker={"color": color_1}      
                ))
        
agg_forecast_fig.add_trace(go.Bar(
                x=[i for i in range(145, 170)],
                y=result['Pred'],
                name='Predicted',
                marker={"color": color_2}      
                ))

agg_forecast_fig.update_layout(
            autosize=False,
            plot_bgcolor="rgb(255, 255, 255, 0)",
            bargap=0.09,
            bargroupgap=0.02,
            dragmode="pan",
            height=400,
            width=1400,
            hovermode="closest",
            legend={
                "x": 0.1,
                "y": -0.08,
                "bgcolor": "rgb(255, 255, 255, 0)",
                "borderwidth": 0,
                "font": {"size": 12},
                "orientation": "h",
            },
            margin={
                "r": 0,
                "t": 50,
                "b": 40,
                "l": 0,
                "pad": 0,
            },
            showlegend=True,
            title=f"Aggregate Orders - Actual & Predicted",
            title_x=0.5,
            titlefont={"size": 20},
            xaxis={
                "autorange": False,
                "nticks": 50,
                "range": [-0.5, 30.5],
                "tickangle": -90,
                "showgrid": False,
                "tickfont": {"size": 10},
                "tickmode": "linear",
                "ticks": "",
                "title": "Day of Year",
                "type": "category",
            },
            yaxis={
                "autorange": True,
                "linecolor": "rgb(176, 177, 178)",
                "nticks": 10,
                "range": [
                    -1283.8982436029166,
                    3012.5614936594166,
                ],
                "showgrid": True,
                "gridcolor": "rgb(220, 220, 220)",
                "showline": True,
                "tickfont": {"size": 12},
                "ticks": "outside",
                "title": "",
                "type": "linear",
                "zeroline": True,
                "zerolinecolor": "rgb(176, 177, 178)",
            },
        )


forecast_1 = dbc.Col([
                dbc.Row(children=[
        dbc.Col([
            dbc.CardDeck([
                    dbc.Card([
        dbc.CardHeader(
            dcc.Markdown(
                """
               The forecasting model was trained on past data and predictions were made with a gap of 14 days from the last training day.

               Profit function is defined as:   Profit = (units_sold x price) - (units_overstock x price x 0.6)
       
                """
                            )    
                        ),
                    ],
                        color="info",
                        outline=True,
                    ),
                ])
            ], width=8),
        dbc.Col([
                dbc.CardDeck([
                    dbc.Card(
                    dbc.CardBody([
                    html.P("Model RMSE", className="card-title"),
                    html.H4("69.232", className="card-text"),
                ]),
                color="primary",
                outline=True,
            ),
                dbc.Card(
                    dbc.CardBody([
                    html.P("Model Profit", className="card-title"),
                    html.H4("4527594.66", className="card-text"),
                ]),
                color="primary",
                outline=True,
            )
        ])
        ], width=4)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    html.Div([
                    dcc.Graph(figure=agg_forecast_fig),
                    ]),width=8), 
                ])
            ])


forecast_2 = dbc.Col([
                dbc.Row(children=[
                    dbc.Col([
                    dbc.Label('Item Id.'),
                    dcc.Dropdown(
                    id='item-dropdown',
                    value=item_list[0],
                    multi=False,
                    options=[{'label': col, 'value': col} for col in item_list]),
                    dbc.FormText('Select an item to view orders')
                      ], width=3),
                    dbc.Col([], width=5),
                    dbc.Col([
            dbc.CardDeck([
                dbc.Card(
                    dbc.CardBody([
                    html.P("Item RMSE", className="card-title"),
                    html.H4(id='item-rmse', className="card-text"),
                ]),
                color="primary",
                outline=True,
            ),
                dbc.Card(
                    dbc.CardBody([
                    html.P("Item Profit", className="card-title"),
                    html.H4(id='item-profit', className="card-text"),
                ]),
                color="primary",
                outline=True,
            )
        ])
        ], width=4)        
            ]),
            html.Br(),
            dbc.Row(children = [
                dbc.Col(
                    html.Div([
                    dcc.Graph(id='item-forecast'),
                    ]),width=12)  
            ])
        ])


model_content = dbc.Card(
    dbc.CardBody([
        html.Br(),
        forecast_1,
        html.Br(),
        html.Br(),
        forecast_2
    ]),color="primary", outline=True,
)


@app.callback(
    Output('item-daily-chart', 'figure'),
    Output('item-month-chart', 'figure'),
    Input('item-id-dropdown', 'value'))

def item_chart(item_id):

    fig_item_day = go.Figure()

    fig_item_day.add_trace(go.Bar(
                    x=agg_orders_day[agg_orders_day['itemID']==item_id]['day_of_year'],
                    y=agg_orders_day[agg_orders_day['itemID']==item_id]['order'],
                    marker={"color": color_1},
                    name="Total Orders"
                ))

    fig_item_day.add_trace(go.Scatter(
                    x=agg_orders_day[agg_orders_day['itemID']==item_id]['day_of_year'],
                    y=agg_orders_day[agg_orders_day['itemID']==item_id]['salesPrice'],
                    hoverinfo="y",
                    line={
                        "color": "#e41f23",
                        "dash": "dot",
                        "width": 2,
                    },
                    marker={
                        "maxdisplayed": 0,
                        "opacity": 0,
                    },
                    name="Sales Price"))
        

    fig_item_day.update_layout(
                autosize=False,
                plot_bgcolor="rgb(255, 255, 255, 0)",
                bargap=0.5,
                dragmode="pan",
                height=390,
                width=1050,
                hovermode="closest",
                legend={
                    "x": 0.1,
                    "y": -0.08,
                    "bgcolor": "rgb(255, 255, 255, 0)",
                    "borderwidth": 0,
                    "font": {"size": 12},
                    "orientation": "h",
                },
                margin={
                    "r": 0,
                    "t": 50,
                    "b": 40,
                    "l": 0,
                    "pad": 0,
                },
                showlegend=True,
                title=f"Item {item_id}: Aggregate Orders - Daily ",
                title_x=0.5,
                titlefont={"size": 20},
                xaxis={
                    "autorange": False,
                    "nticks": 50,
                    "range": [-0.5, 60.5],
                    "tickangle": -90,
                    "showgrid": False,
                    "tickfont": {"size": 10},
                    "tickmode": "linear",
                    "ticks": "",
                    "title": "Day of Year",
                    "type": "category",
                },
                yaxis={
                    "autorange": True,
                    "linecolor": "rgb(176, 177, 178)",
                    "nticks": 10,
                    "range": [
                        -1283.8982436029166,
                        3012.5614936594166,
                    ],
                    "showgrid": True,
                    "gridcolor": "rgb(220, 220, 220)",
                    "showline": True,
                    "tickfont": {"size": 12},
                    "ticks": "outside",
                    "title": "",
                    "type": "linear",
                    "zeroline": True,
                    "zerolinecolor": "rgb(176, 177, 178)",
                },
            )

    # monthly

    fig_item_month = go.Figure()

    fig_item_month.add_trace(go.Bar(
                    x=agg_orders_month[agg_orders_month['itemID']==item_id]['month'],
                    y=agg_orders_month[agg_orders_month['itemID']==item_id]['order'],
                    marker={"color": color_1}
                ))

    fig_item_month.add_trace(go.Scatter(
                    x=agg_orders_month[agg_orders_month['itemID']==item_id]['month'],
                    y=agg_orders_month[agg_orders_month['itemID']==item_id]['salesPrice'],
                    hoverinfo="y",
                    line={
                        "color": "#e41f23",
                        "dash": "dot",
                        "width": 2,
                    },
                    marker={
                        "maxdisplayed": 0,
                        "opacity": 0,
                    }
                ))

    fig_item_month.update_layout(
                autosize=False,
                plot_bgcolor="rgb(255, 255, 255, 0)",
                bargap=0.3,
                dragmode="pan",
                height=400,
                width=360,
                hovermode="closest",
                margin={
                    "r": 10,
                    "t": 50,
                    "b": 40,
                    "l": 0,
                    "pad": 0,
                },
                showlegend=False,
                title="Monthly",
                title_x=0.5,
                titlefont={"size": 20},
                xaxis={
                    "autorange": False,
                    "nticks": 10,
                    "range": [-0.5, 6],
                    "tickangle": -90,
                    "showgrid": False,
                    "tickfont": {"size": 10},
                    "tickmode": "array",
                    "ticks": "",
                    "title": "",
                    "tickvals": ['01-2018', '02-2018', '03-2018', '04-2018', '05-2018', '06-2018'],
                    "ticktext": ["Jan-18", "Feb-18", "Mar-18", "Apr-18", "May-18", "Jun-18"],
                    "type": "category",
                },
                yaxis={
                    "autorange": True,
                    "linecolor": "rgb(176, 177, 178)",
                    "nticks": 10,
                    "range": [
                        -1283.8982436029166,
                        3012.5614936594166,
                    ],
                    "showgrid": True,
                    "gridcolor": "rgb(220, 220, 220)",
                    "showline": True,
                    "tickfont": {"size": 12},
                    "ticks": "outside",
                    "title": "",
                    "type": "linear",
                    "zeroline": True,
                    "zerolinecolor": "rgb(176, 177, 178)",
                },
            ),

    return (
        fig_item_day,
        fig_item_month
    )


@app.callback(
    Output("sales-price", "children"),
    Output("promotion-price", "children"),
    Output("retail-price", "children"),
    Output("customer-rating", "children"),
    Output("manufacturer", "children"),
    Input("item-id-dropdown", "value"),
)


# Setup app

def cards_builder(item_id):

    # Cards
    sales_price = "{:,.2f}".format(mean_price_daily[mean_price_daily['itemID']==item_id]['salesPrice'].mean())                   
    promotion_price = items[items['itemID']==item_id]['simulationPrice']
    retail_price = items[items['itemID']==item_id]['recommendedRetailPrice']
    customer_rating = items[items['itemID']==item_id]['customerRating']
    manufacturer = items[items['itemID']==item_id]['manufacturer']

    return (
    sales_price,
    promotion_price,
    retail_price,
    customer_rating,
    manufacturer,  
    )

# Price Chart

@app.callback(
    Output('price-chart', 'figure'),
    Input('price-dropdown', 'value'))

def price_chart(price_type):

    fig_price = go.Figure()

    if 'Simulation' in price_type:
        fig_price.add_trace(
            go.Histogram(
                x=items['simulationPrice'],
                marker={"color": color_1},
                name="Simulation Price"
            ))
    
    if 'Retail' in price_type:
        fig_price.add_trace(
            go.Histogram(
                x=items['recommendedRetailPrice'],
                marker={"color": color_2},
                 name="Retail Price"
            ))

    fig_price.update_layout(
                    barmode='stack',
                    plot_bgcolor="rgb(255, 255, 255, 0)",
                    bargap=0,
                    height=400,
                    width=700,
                    dragmode="pan",
                    hovermode="closest",
                    autosize=False,
                    legend={
                        "x": 0.8,
                        "y": 1,
                        "bgcolor": "rgb(255, 255, 255, 0)",
                        "borderwidth": 0,
                        "font": {"size": 12},
                        "orientation": "v",
                    },
                    margin={
                        "r": 0,
                        "t": 30,
                        "b": 30,
                        "l": 30,
                        "pad": 0,
                    },
                    showlegend=True,
                    title="Price Distribution",
                    titlefont={"size": 20},
                    title_x=0.5,
                    xaxis={
                        "nticks": 50,
                        "range": [-0.5, 500.5],
                        "tickangle": -90,
                        "showgrid": False,
                        "tickfont": {"size": 10},
                        "ticks": "",
                        "title": "Price",
                    },
                    yaxis={
                        "autorange": True,
                        "linecolor": "rgb(128, 128, 128)",
                        "showgrid": True,
                        "gridcolor": "rgb(220,220,220)",
                        "showline": True,
                        "tickfont": {"size": 12},
                        "ticks": "outside",
                        "title": "",
                        "type": "linear",
                        "zeroline": True,
                        "zerolinecolor": "rgb(176, 177, 178)"
                    }
            )      

    return (
        fig_price
    )

# Ratings Chart

@app.callback(
    Output('fig-rating', 'figure'),
    Input('manuf-id-dropdown', 'value'))

def price_chart(manuf_id):

    fig_rating = go.Figure()

    fig_rating.add_trace(
        go.Scatter(
                x=items[items['manufacturer']==manuf_id]['itemID'],
                y=items[items['manufacturer']==manuf_id]['customerRating'],
                marker={
                        "color": "rgb(255, 0, 0)",
                        "symbol": "diamond",
                    },
                    mode="markers",
                    visible=True,
                    name="Rating",
                ))

    fig_rating.update_layout(
                    plot_bgcolor="rgb(255, 255, 255, 0)",
                    height=420,
                    width=700,
                    dragmode="pan",
                    hovermode="x unified",
                    autosize=False,
                    legend={
                        "x": 0.1,
                        "y": -0.15,
                        "bgcolor": "rgb(255, 255, 255, 0)",
                        "borderwidth": 0,
                        "font": {"size": 12},
                        "orientation": "v",
                    },
                    margin={
                        "r": 0,
                        "t": 30,
                        "b": 30,
                        "l": 30,
                        "pad": 0,
                    },
                    showlegend=True,
                    title="Customer Ratings",
                    titlefont={"size": 20},
                    title_x=0.5,
                    xaxis={
                        "tickangle": -90,
                        "showgrid": False,
                        "tickfont": {"size": 10},
                        "ticks": "",
                        "title": "Item ID",
                    },
                    yaxis={
                        "autorange": True,
                        "showgrid": True,
                        "gridcolor": "rgb(220,220,220)",
                        "showline": True,
                        "tickfont": {"size": 12},
                        "ticks": "outside",
                        "title": "",
                        "type": "linear",
                        "zeroline": True,
                        "zerolinecolor": "rgb(176, 177, 178)"
                    }
            )      

    return (
        fig_rating
    )


@app.callback(
    Output("item-forecast", "figure"),
    Input("item-dropdown", "value"),
)


def item_forecast_chart(item_id):

    item_forecast_fig = go.Figure()

    item_forecast_fig.add_trace(go.Bar(
                    x=[i for i in range(145, 170)],
                    y=result[result['itemID']==item_id]['Truth'],
                    name='Actual',
                    marker={"color": color_1}      
                    ))
            
    item_forecast_fig.add_trace(go.Bar(
                    x=[i for i in range(145, 170)],
                    y=result[result['itemID']==item_id]['Pred'],
                    name='Predicted',
                    marker={"color": color_2}      
                    ))

    item_forecast_fig.update_layout(
                autosize=False,
                plot_bgcolor="rgb(255, 255, 255, 0)",
                bargap=0.09,
                bargroupgap=0.02,
                dragmode="pan",
                height=400,
                width=1400,
                hovermode="closest",
                legend={
                    "x": 0.1,
                    "y": -0.08,
                    "bgcolor": "rgb(255, 255, 255, 0)",
                    "borderwidth": 0,
                    "font": {"size": 12},
                    "orientation": "h",
                },
                margin={
                    "r": 0,
                    "t": 50,
                    "b": 40,
                    "l": 0,
                    "pad": 0,
                },
                showlegend=True,
                title=f"Item {item_id}: Orders - Actual & Predicted",
                title_x=0.5,
                titlefont={"size": 20},
                xaxis={
                    "autorange": False,
                    "nticks": 50,
                    "range": [-0.5, 30.5],
                    "tickangle": -90,
                    "showgrid": False,
                    "tickfont": {"size": 10},
                    "tickmode": "linear",
                    "ticks": "",
                    "title": "Day of Year",
                    "type": "category",
                },
                yaxis={
                    "autorange": True,
                    "linecolor": "rgb(176, 177, 178)",
                    "nticks": 10,
                    "range": [
                        -1283.8982436029166,
                        3012.5614936594166,
                    ],
                    "showgrid": True,
                    "gridcolor": "rgb(220, 220, 220)",
                    "showline": True,
                    "tickfont": {"size": 12},
                    "ticks": "outside",
                    "title": "",
                    "type": "linear",
                    "zeroline": True,
                    "zerolinecolor": "rgb(176, 177, 178)",
                },
            )

    return (
    item_forecast_fig
    )



@app.callback(
    Output("item-rmse", "children"),
    Output("item-profit", "children"),
    Input("item-dropdown", "value"),
)


def item_forecast_chart(item_id):

    truth = result[result['itemID']==item_id]['Truth']
    pred = result[result['itemID']==item_id]['Pred']

    promotion_price = items[items['itemID']==item_id]['simulationPrice']
    pred_act = np.where(pred > 0, pred, 0)
    pred_act = np.round(pred_act).astype('int')
    sale = np.minimum(truth, pred_act)

    overstock = pred_act - truth
    overstock[overstock < 0] = 0

    revenue = sale * promotion_price
    fee     = overstock * promotion_price * 0.6
    profit  = revenue - fee

    rmse = "{:,.3f}".format(np.sqrt(mean_squared_error(pred, truth)))   
    profit = "{:,.2f}".format(profit.sum())   

    return(
        rmse, profit
    )


# Setup app and layout/frontend

dashboard_logo = 'assets/ecological.png'
encoded_image = base64.b64encode(open(dashboard_logo, 'rb').read())

server = app.server

app.layout = dbc.Container([
    dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height='30px')),
                        dbc.Col(dbc.NavbarBrand('Demand Forecasting Dashboard', className='ml-2')),
                    ],
                    align='center',
                    no_gutters=True,
                ),
            ),
            dbc.NavbarToggler(),
            dbc.Collapse(collapse_button, navbar=True)
        ],
        color='light', dark=False,
        style={'border-radius': '5px'}
    ),
    html.Br(),
    collapse,
    dbc.Row([
        dbc.Col([
            dbc.Tabs(
                [
                    dbc.Tab(eda_content, label='Basic EDA', tab_id='tab-basic-eda'), 
                    dbc.Tab(model_content, label='Forecast', tab_id='tab-model'),
                ],
                id='card-tabs',
                active_tab='tab-basic-eda'
            )
        ])
    ]),
    html.Hr(),
    html.P('This app follows MIT license',
           style={'font-size': '80%'})
], fluid=True, style={'border-width': '10'})



if __name__ == "__main__":
    app.run_server(debug=True)
























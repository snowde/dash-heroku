# coding: utf-8

import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import multiple_charts as mc
import input as inp
import polar_figure as pf
import polar_figure_2 as pf2
import charting_words as cw
import frequency_word_chart as fwc
import glassdoor_chart as gc
import chart_ratings as cr

from plotly import graph_objs as go
from datetime import datetime as dt
import json
import json
import pandas as pd
import os
from flask import Flask
from six.moves import cPickle as pickle #for performance
import treemap as tm

ticker = "BJRI"
#######

## This is to import csv files from dropbox ####

import pandas as pd
from stock_narration import describe
import frames as fm
from figures import figs

##
def db_frame(url):
    url = url.replace("dl=0", "dl=1")  # dl=1 is important

    import urllib.request
    u = urllib.request.urlopen(url)
    data = u.read()
    u.close()

    def find_between_r(s, first, last):
        try:
            start = s.rindex(first) + len(first)
            end = s.rindex(last, start)
            return s[start:end]
        except ValueError:
            return ""

    filename = find_between_r(url, "/", "?")

    with open(filename, "wb") as f:
        f.write(data)

    ff = pd.read_excel(filename)
    return ff

#go
s_metrics_df = fm.s_metrics_df
c_metrics_df = fm.c_metrics_df



r = 5
if r>4:
    employee_sentiment = "happy"
else:
    employee_sentiment = "unhappy"

dict = {

    "title":"BJ’s Restaurant & Brewhouse",
    "location":"Jacksonville",
    "employees":"Employees are " + employee_sentiment + "." + "The company then bought 26.",
    "customers":"Customers are happy. The company then bought 26.",
    "shareholders":"Shareholders are happy. The company then bought 26.",
    "management":"Management is performing well. The company then bought 26."

}
#


from datetime import datetime, timedelta

now = datetime.now()

#stock_price_desc = describe


server = Flask('my app')


def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

##
#df_perf_summary = pd.read_csv("17530.csv")

df_perf_summary = fm.fin_met("BJRI","CMG")

modifed_perf_table = make_dash_table(df_perf_summary)

modifed_perf_table.insert(
    0, html.Tr([
        html.Td([]),
        html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
        html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)

# Function To Import Dictionary and Open IT.
def load_dict(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pd.read_pickle(f)
    return ret_di

# And the specification of this table
dict_frames = load_dict('./data.pkl') # Much rather use this one


df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544.csv')
df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542.csv')
df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540.csv')
df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538.csv')

available_benchmarks = ["MENU ETF","Filtered ETF","Chipotle"]
available_locations = ["All","Jacksonville","Wisconsin","Michigan"]

tickers_loca = {"All":ticker,"Jacksonville":ticker,"Wisconsin":ticker,"Michigan":ticker}
tickers_bench ={"MENU ETF":"CMG", "Filtered ETF":"CMG","Chipotle":"CMG"}

app = dash.Dash('GS Bond II Portfolio', server=server,
                url_base_pathname='/dash/gallery/goldman-sachs-report/', csrf_protect=False)
##
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


# Describe the layout, or the UI, of the app
app.layout = html.Div([

    html.Div([  # page 1

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 1

            # Row 1 (Header)

            html.Div([

                html.Div([
                    #html.H5(
                    ##
                    #    dict["title"] + " 4-D Report"),
                    html.H5(id='title'),

                    html.H6(id='location',
                            style={'color': '#7F90AC'}),
                    html.Div([


                        html.Div([
                            dcc.Dropdown(
                                id='locas',
                                options=[{'label': i, 'value': i} for i in available_locations],
                                value="All",
                                clearable=False,
                                className="dropper"


                            )
                        ], style={'background-color':'#a9a9a9','color':'rgb(217, 224, 236)','float':'left', 'padding-right': '0cm', 'width': '20%'}),

                        html.Div([
                            html.Button('SWAP', id='button_swap', n_clicks=0, style={'height': '3.3em', 'float': 'center', 'color':'rgb(217, 224, 236)'})
                        ], style={'padding-left': '0.8cm', 'padding-right': '0.8cm','float':'left'}),

                        html.Div([
                            dcc.Dropdown(
                                id='benchy',
                                options=[{'label': i, 'value': i} for i in available_benchmarks],
                                value='MENU ETF',
                                clearable=False,
                                className="dropper"


                            )
                        ], style={'background-color':'#a9a9a9','color':'rgb(217, 224, 236)','width': '80%','float':'left','width': '20%'}),
                        html.Div([html.H3('3.6/5')],style={'padding-left': '1.2cm','float':'left'})
                        # , 'float': 'right', 'display': 'inline-block'
                    ], style={'padding-top': '0.3cm', 'padding-left': '0cm'},
                        className="double_drop"),

                ], className="nine columns padded"),

                html.Div([
                    html.H1(
                        [html.Span(str(now.month), style={'opacity': '0.5'}), html.Span(str(now.year)[2:])]),
                    html.H6('Monthly Interactive Update')
                ], className="three columns gs-header gs-accent-header padded", style={'float': 'right'}),

            ], className="row gs-header gs-text-header"),


            html.Br([]),

            html.Div([

                    html.Div([html.H6(["Executive Summary"], style={"float":"left","padding-right":"0.2cm"}),
                    html.A("info", href='http://4d.readthedocs.io/en/latest/text/executive_summary.html#executive-summary', target="_blank")
                        ],className="gs-header gs-table-header padded"),

                      html.P(inp.exec, style={"padding-top":"1mm"})]),


            # Row 2

            html.Div([

                html.Div([

                    html.H6(id="profile",className="gs-header gs-text-header padded"),

                    html.Strong("Employees pg 4"),
                    html.P(dict["employees"],
                           className='blue-text'),

                    html.Strong(
                        'Customers pg 6'),
                    html.P(dict["customers"],
                           className='blue-text'),

                    html.Strong('Shareholders pg 8'),
                    html.P(dict["shareholders"],
                           className='blue-text'),

                    html.Strong('Management pg 10'),
                    html.P(dict["management"],
                           className='blue-text'),

                ], className="four columns"),

                html.Div([
                    html.H6(["Shareholder Performance"],
                            className="gs-header gs-table-header padded"),
                    #html.Iframe(src="https://plot.ly/~snowde/36.embed?modebar=false&link=false&autosize=true", \
                    #            seamless="seamless", style={'border': '0', 'width': "100%", 'height': "250"}),

                dcc.Graph(
                    id='stock_plot',style={'border': '0', 'width': "100%", 'height': "250"},
                    config={'displayModeBar': False}
                )
                ], className="eight columns"),
            ], className="row "),

            # Row 2.5, s

            html.Div([

                html.Div([


                    html.H6('Stakeholder Metrics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(s_metrics_df), style={'marginBottom': 5},
                               className='tiny-header'),
                    html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                    html.H6('Company Metrics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(c_metrics_df), style={'marginBottom': 5},
                               className='tiny-header'),
                ], className="four columns"),



                html.Div([
                    html.P(id='stock_plot_desc', style={"padding-top":"1.2mm"}),
                ], className="eight columns"),
                html.Div([

                    html.H6("Financial Performance",
                            className="gs-header gs-table-header padded"),
                    html.Table(modifed_perf_table,id="mgmt_perf", className="reversed")
                ], className="eight columns"),

            ], className="row "),

            # Row 3#


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 2

                # Row 1 (Header)

                html.Div([
                    html.H6(["Executive Advice"],
                            className="gs-header gs-table-header padded"),

                        ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 1

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 1

                # Row 1 (Header)

                html.Br([]),

                html.Div([html.H6(["Trend Analysis"],
                                className="gs-header gs-table-header padded"),
                          html.P(inp.exec, style={"padding-top":"1mm"}),

                            html.Div([
                                dcc.Tabs(
                                    tabs=[{'label':"Overall" , 'value':"Overall" },
                                          {'label':"Employee" , 'value':"Employee" },
                                          {'label':"Management" , 'value':"Management" },
                                          {'label':"Shareholders" , 'value':"Shareholders" },
                                          {'label':"Customers" , 'value':"Customers" },
                                          {'label':"Search" , 'value':"Search" },
                                    ],
                                    value=3,
                                    id='tabs'
                                ),
                                html.Div(id='tab-output')
                            ], style={
                                'width': '100%',
                                'fontFamily': 'Sans-Serif',
                                'margin-left': 'auto',
                                'margin-right': 'auto'
                            })

                         ]),

                # Row 2
                # Row 2.5, s

                html.Div([

                    html.Div([


                        html.H6('Stakeholder Metrics',
                                className="gs-header gs-text-header padded"),
                        html.Table(make_dash_table(s_metrics_df), style={'marginBottom': 5},
                                   className='tiny-header'),
                        html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                        html.H6('Financial Metrics',
                                className="gs-header gs-text-header padded"),
                        html.Table(make_dash_table(c_metrics_df), style={'marginBottom': 5},
                                   className='tiny-header'),
                    ], className="four columns"),


                    html.Div([

                        html.H6("Management Performance",
                                className="gs-header gs-table-header padded"),
                        html.Table(modifed_perf_table,id="mgmt_perf", className="reversed")
                    ], className="eight columns"),

                ], className="row "),

                # Row 3#


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

                html.A(['Print PDF'],
                       className="button no-print",
                       style={'position': "absolute", 'top': '-40', 'right': '0'}),

                html.Div([  # subpage 2

                    # Row 1 (Header)

                    html.Div([
                        html.H6(["Sensitivity and Valuation Analysis"],
                                className="gs-header gs-table-header padded"),

                            ]),

        ], className="subpage"),

    ], className="page"),


    html.Div([  # page 3

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                    html.H6(["Competitor Analysis"],
                            className="gs-header gs-table-header padded") ]),

            dcc.Graph(figure=pf.figs_polar(ticker,"bench", ticker), config={'displayModeBar': False}, id='comp_plot',style={'border': '0', 'width': "100%", 'height': "250"}),


        ], className="subpage"),

            # Row 2

            html.Div(html.P(inp.exec, style={"padding-top":"1mm"}))

    ], className="page"),

    html.Div([  # page 5

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 2

                # Row 1 (Header)

                    html.Div([
                        html.H6(["Employee Analysis"],
                                className="gs-header gs-table-header padded")]),

                        gc.layout,

        ], className="subpage" ),

    ],className="page"),

    html.Div([  # page 4

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Customer Analysis"],
                        className="gs-header gs-table-header padded")]),

            dcc.Graph(figure=fwc.four_figs(), id='words_one', config={'displayModeBar': False},
                      style={'padding-left': '0cm','margin-right': '100px','border': '0', 'width': "100%", 'height': "550"}),

        ], className="subpage"),

        # Row 2

        html.Div(html.P(inp.exec, style={"padding-top": "1mm"}))

    ], className="page"),



    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Shareholder Analysis"],
                        className="gs-header gs-table-header padded"),

                    ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Management Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Dimensional Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Appendix Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 3

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([

                # Data tables on this page:
                # ---
                # df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')
                # df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')
                # df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')
                # df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

                # Column 1

                html.Div([
                    html.H6('Financial Information',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(df_fund_info), id="table1"),

                    html.H6('Fund Characteristics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(df_fund_characteristics)),

                    html.H6('Fund Facts',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(df_fund_facts)),

                ], className="four columns"),

                # Column 2##

                html.Div([
                    html.H6('Sector Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17560.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                    html.H6('Country Bond Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_bond_allocation)),

                ], className="four columns"),

                # Column 3

                html.Div([
                    html.H6('Top 10 Currency Weights (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17555.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                    html.H6('Credit Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17557.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                ], className="four columns"),

            ], className="row"),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 2

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 2

                # Row 1 (Header)

                html.Div([
                        html.H6(["Company Financials"],
                                className="gs-header gs-table-header padded")]),

                mc.layout,

                # Row 2

                html.Div([html.P(inp.exec, style={"padding-top":"1mm"}),

                          html.Div([dcc.Graph(
                              id='first_tree',
                              config={'displayModeBar': False},
                              style={'autosize': 'False', 'margin-top': '-100px', 'padding-right': '4cm', 'border': '0',
                                     'width': "20%", 'height': "20%"})

                          ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                                    'padding-right': '4cm', 'width': "20%", 'height': "20%"}),

                          html.Div([dcc.Graph(
                              id='third_tree',
                              config={'displayModeBar': False},
                              style={'autosize': 'False', 'margin-top': '-100px', 'padding-top': '0cm',
                                     'padding-left': '4cm', 'border': '0', 'width': "20%", 'height': "20%"})

                          ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                                    'padding-right': '0cm', 'width': "20%", 'height': "20%"}),
                          ],style={'z-index':'3'}),


        ], className="subpage" ),

    ],className="page")

])

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

#'https://codepen.io/chriddyp/pen/bWLwgP.css',##
# If you upload css you have to reapload it after github to git raw.
# fuckit i JUST STORED IT IN KERAS
#https://github.com/snowde/keras/blob/master/just.css

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                #"https://www.dropbox.com/s/7zx0pqn3eqql7b1/this.css?dl=1"
                "https://cdn.rawgit.com/snowde/keras/c59812f7/just.css",
                #"https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = [
               "https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/snowde/keras/2b7d6742/new_java.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js",
                ]

for js in external_js:
    app.scripts.append_script({"external_url": js})



# Call Backs

@app.callback(
    dash.dependencies.Output('stock_plot', 'figure'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_fig(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        fig = figs(the_location, the_benchmark, False)
    else:
        fig = figs(the_benchmark, the_location, True)
    return fig


@app.callback(
    dash.dependencies.Output('stock_plot_desc', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_desc(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        desc = describe(the_location, the_benchmark, False)
    else:
        desc = describe(the_benchmark, the_location, True)
    return desc


@app.callback(
    dash.dependencies.Output('title', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_title(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        title = dict["title"] + " 4-D Report"
    else:
        title = str(the_benchmark) + " 4-D Report"
    return title

@app.callback(
    dash.dependencies.Output('location', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_title(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        title = str(the_location) + " Location"
    else:
        title = str(the_benchmark) + " Locations"
    return title


@app.callback(
    dash.dependencies.Output('profile', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_title(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        title = str(the_location) + " Profile"
    else:
        title = str(the_benchmark) + " Profile"
    return title


@app.callback(
    dash.dependencies.Output('mgmt_perf', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_table(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        df_perf_summary = fm.fin_met(tickers_loca[the_location], tickers_bench[the_benchmark])
    else:
        df_perf_summary = fm.fin_met(tickers_bench[the_benchmark], tickers_loca[the_location])
    modifed_perf_table = make_dash_table(df_perf_summary)

    modifed_perf_table.insert(
        0, html.Tr([
            html.Td([]),
            html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
            html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
    )
    return modifed_perf_table

@app.callback(
    Output('filtered-content', 'children'),
    [Input('category-filter', 'value'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter( var, req, stu, ben):
    print(req, stu, ben)

    df = dict_frames[ben, req, stu]

    highlight = list(df.drop("year",axis=1).columns.values)
    print(highlight)

    if stu in ["Normalised", "Original"]:
        highlight = list(df.ix[:, :5].columns.values)

    highlight = highlight + var
    print(highlight)
    figure = mc.create_figure(highlight,df,req, stu)

    for trace in figure['data']:
        trace['hoverinfo'] = 'text'

    return dcc.Graph(
        id='filtered-graph',
        figure=figure,config={'displayModeBar': False}
    )
##
@app.callback(
    Output('category-filter', 'options'),
    [Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(req, stu, ben):
    # print(per, req, stu, ben)

    df = dict_frames[ben, req, stu]
    highlight = list(df.drop("year", axis=1).columns.values)

    return [{'label': i, 'value': i} for i in highlight]


@app.callback(
    Output('first_tree', 'figure'),
    [Input('request', 'value'),
     ])
def filter(req):
    df = dict_frames["BJRI", req, "Original"]
    print(df)
    return tm.treemap(df)
###
@app.callback(
    Output('third_tree', 'figure'),
    [Input('request', 'value'),
     ])
def filter(req):
    df = dict_frames["CMG", req, "Original"]
    print(df)
    return tm.treemap(df)

@app.callback(
    Output('graphed', 'figure'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2( goo, time, many, norm, bench):
    #print(per, req, stu, ben)

    figure = gc.chart_gd(goo, time, many, norm, bench)


    return figure

@app.callback(
    Output('text_sum', 'value'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2( goo, time, many, norm, bench):
    #print(per, req, stu, ben)

    figure = gc.sum_gd(goo, time, many, norm, bench)
    return figure
##

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):

    layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_overall, config={'displayModeBar': False},
                                 style={"margin-top": "0mm"})])
    if value== "Overall":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_overall, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Employee":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_emp, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Management":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_mgm, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Shareholders":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_sha, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Customers":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_cus, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_search, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])


    return layout

if __name__ == '__main__':
    app.server.run(debug=True, host='127.0.0.1', port=5000)
#
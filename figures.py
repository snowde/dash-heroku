import pandas as pd
import input

from datetime import datetime, timedelta

import plotly.plotly as py
from plotly.graph_objs import *

#

def figs(loca, bench,swap):

    tick = " (BJRI) "
    company = "BJ's"

    ben_frs_dict = {"MENU ETF": input.df_final, "Filtered ETF": input.df_final_filt, "Chipotle": input.df_final_one}

    if swap == True:
        df_tick = ben_frs_dict[loca]
        df_final = input.df_tick
        tick = " "
        bench = company
        company = loca

    else:
        df_tick = input.df_tick
        df_final = ben_frs_dict[bench]

    df_final["date"] = pd.to_datetime(df_final["date"], format="%Y-%m-%d")
    df_tick["date"] = pd.to_datetime(df_tick["date"], format="%Y-%m-%d")

    py.sign_in('snowde', 'm12EGGpG9bqMssuzLnjY')
    trace1 = {
        "x": df_tick["date"],
        "y": df_tick["close"],
        "line": {
            "color": "rgb(140, 15, 7)",
            "width": 3
        },
        "mode": "lines",
        "name": company,
        "type": "scatter",
        "uid": "4cd1a4"
    }
    trace2 = {
        "x": df_final["date"],
        "y": df_final["close"],
        "connectgaps": True,
        "line": {
            "color": "rgb(22, 60, 109)",
            "dash": "dash",
            "width": 3
        },
        "mode": "lines",
        "name": bench,
        "type": "scatter",
        "uid": "f7fed3"
    }
    data = Data([trace1, trace2])
    layout = {
        "autosize": True,
        "font": {"family": "Raleway"},
        "hovermode": "compare",
        "legend": {
            "x": 0.45,
            "y": 0.05,
            "bgcolor": "rgba(255, 255, 255, 0.5)",
            "orientation": "v"
        },
        "margin": {
            "r": 0,
            "t": 10,
            "b": 30,
            "l": 35,
            "pad": 0
        },
        "plot_bgcolor": "rgb(217, 224, 236)",
        "showlegend": True,
        "title": "",
        "titlefont": {
            "family": "Raleway",
            "size": 12
        },
        "xaxis": {
            "autorange": False,
            "gridcolor": "rgb(255, 255, 255)",
            "range": [str(min([df_final["date"].min(), df_tick["date"].min()]))[:10],
                      str(max([df_final["date"].max() + timedelta(days=200), df_tick["date"].max() + timedelta(days=200)]))[
                      :10]],
            "showline": True,
            "tickfont": {"color": "rgb(68, 68, 68)"},
            "tickformat": "%b %Y",
            "ticks": "outside",
            "title": "",
            "type": "date"
        },
        "yaxis": {
            "autorange": False,
            "gridcolor": "rgb(255, 255, 255)",
            "nticks": 11,
            "range": [int(min([df_final["close"].min(), df_tick["close"].min()]) - 40),
                      int(max([df_final["close"].max(), df_tick["close"].max()]) + 10)],
            "showline": True,
            "ticks": "outside",
            "title": "",
            "type": "linear"
        }
    }
    fig = Figure(data=data, layout=layout)
    # plot_url = py.plot(fig)
    return fig
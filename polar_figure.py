# Get this figure: fig = py.get_figure("https://plot.ly/~1beb/3/")
# Get this figure's data: data = py.get_figure("https://plot.ly/~1beb/3/").get_data()
# Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="plot from API", fileopt="extend")

# Get figure documentation: https://plot.ly/python/get-requests/
# Add data documentation: https://plot.ly/python/file-options/

# If you're using unicode in your file, you may need to specify the encoding.
# You can reproduce this figure in Python with the following code!

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api


import pandas as pd
import numpy as np
import input

from datetime import datetime, timedelta

import plotly.plotly as py
from plotly.graph_objs import *

def figs_polar(loca, bench,swap):

    trace1 = {"type": "scatter"}
    trace2 = {
      "x": [0, 0],
      "y": [0, 0],
      "line": {
        "color": "#d3d3d3",
        "dash": "3px"
      },
      "showlegend": False,
      "type": "scatter"
    }

    plots_dict = {}
    plots_dict["BJRI", "Employees"] = 0.5
    plots_dict["BJRI", "Managers"] = 0.8
    plots_dict["BJRI", "Shareholders"] = 0.7
    plots_dict["BJRI", "Customers"] = 0.5

    plots_dict["CMG", "Employees"] = 0.7
    plots_dict["CMG", "Managers"] = 0.4
    plots_dict["CMG", "Shareholders"] = 0.9
    plots_dict["CMG", "Customers"] = 0.6

    key_tick = list(pd.DataFrame(np.array(list(plots_dict.keys())).reshape(-1, 2))[0].drop_duplicates().values)

    key_type = list(pd.DataFrame(np.array(list(plots_dict.keys())).reshape(-1, 2))[1].drop_duplicates().values)

    abso = {}
    for key, value in plots_dict.items():
      abso[key] = abs(value)

    max_value = {}
    for r in key_type:
      k = 0
      for i in key_tick:
        max_value[r] = abso[i, r]
        if max_value[r] < k:
          max_value[r] = k
        else:
          k = max_value[r]

    trace26 = {
      "x": [0, 1*plots_dict["BJRI","Customers"], 0, -1*plots_dict["BJRI","Managers"], 0],
      "y": [1*plots_dict["BJRI","Shareholders"], 0, -1*plots_dict["BJRI","Employees"], 0, 1*plots_dict["BJRI","Shareholders"]],
      "hoverinfo": "text",
      "marker": {"color": "#66C2A5"},
      "mode": "lines+markers",
      "name": "BJRI",
      "text": ["2015 Shareholders 54 %", "2015 Customers 43 %", "2015 Employees 27 %","2015 Managers 38 %"],
      "type": "scatter"
    }
    trace27 = {
      "x": [0, 1 * plots_dict["CMG", "Customers"], 0, -1 * plots_dict["CMG", "Managers"], 0],
      "y": [1 * plots_dict["CMG", "Shareholders"], 0, -1 * plots_dict["CMG", "Employees"], 0, 1 * plots_dict["CMG", "Shareholders"]],
      "hoverinfo": "text",
      "marker": {"color": "#8DA0CB"},
      "mode": "lines+markers",
      "name": "CMG",
      "text": ["2016 Shareholders 55 %", "2016 Customers 55 %", "2016 Employees 31 %", "2016 Managers 40 %"],
      "type": "scatter"
    }
    trace28 = {
      "x": [0, 0.16 + max_value["Customers"], 0, -.15 - max_value["Managers"], 0],
      "y": [0.7 + max_value["Shareholders"], 0, -.10 - max_value["Employees"],0, 0.1 + max_value["Shareholders"]],
      "hoverinfo": "none",
      "line": {
        "color": "white",
        "dash": "30px",
        "shape": "spline"
      },
      "mode": "lines+text",
      "showlegend": False,
      "text": ["Shareholders","Customers", "Employees", "Managers","Shareholders"],
      "textposition": "top middle",
      "type": "scatter"
    }

    data = Data([trace1, trace2, trace26, trace27, trace28])
    layout = {
      "autosize": False,
      "height": 400,
      "hovermode": "closest",
      "width": 400,
      "xaxis": {
        "range": [-1.25, 1.25],
        "showgrid": False,
        "showticklabels": False,
        "zeroline": False
      },
      "yaxis": {
        "range": [-1.25, 1.25],
        "showgrid": False,
        "showticklabels": False,
        "zeroline": False
      }
    }
    fig = Figure(data=data, layout=layout)
    #plot_url = py.plot(fig)
    return fig
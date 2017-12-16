import pandas as pd

import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

import squarify


def treemap(df):
    bs = df
    liab = [
        "totalcurrentliabilities",
        "totalnoncurrentliabilities"
    ]

    ass = [
        "netppe",
        "totalcurrentassets",
        "totalnoncurrentassets"
    ]

    equ = [
        "totalcommonequity",
    ]

    tras = bs.T[bs.T.index.isin(["netppe",
                                 "totalnoncurrentassets",
                                 "totalcurrentassets",
                                 "totalcurrentliabilities",
                                 "totalcommonequity",
                                 "totalnoncurrentliabilities"])]

    tras["cat"] = np.where(tras.index.isin(ass), "asset", (
    np.where(tras.index.isin(liab), "liability", (np.where(tras.index.isin(equ), "equity", np.nan)))))

    tras = tras[tras["cat"].isin(["liability", "equity", "asset"])]

    tras = tras.sort_values("cat", ascending=True)

    lit = list(tras.index.values)

    dam = [str(v) for v in ['ppe',
 'ca',
 'nca',
 'ce',
 'cl',
 'ncl']]

    x = 0.
    y = 0.
    width = 100.
    height = 100.

    # values = [500, 433, 78, 25, 25, 7]
    values = list(tras[6].values)



    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = ['rgb(166,206,227)', '#CAFF70', '#CDB7B5',
                    '#EED5B7', 'pink', '#EBEBEB']
    shapes = []
    annotations = []
    counter = 0

    for r in rects:
        shapes.append(
            dict(
                type='rect',
                x0=r['x'],
                y0=r['y'],
                x1=r['x'] + r['dx'],
                y1=r['y'] + r['dy'],
                line=dict(width=2),
                fillcolor=color_brewer[counter]
            )
        )
        annotations.append(
            dict(
                x=r['x'] + (r['dx'] / 2),
                y=r['y'] + (r['dy'] / 2),
                text=dam[counter],
                textangle=15,
                showarrow=False
            )
        )
        counter = counter + 1
        if counter >= len(color_brewer):
            counter = 0

    # For hover text
    trace0 = go.Scatter(
        x=[r['x'] + (r['dx'] / 2) for r in rects],
        y=[r['y'] + (r['dy'] / 2) for r in rects],
        text=[str(v) for v in lit],
        mode='text',
    )


    layout = dict(
        height=350,
        width=350,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        shapes=shapes,
        annotations=annotations,
        hovermode='closest'
    )

    # With hovertext
    figure = dict(data=[trace0], layout=layout)

    # Without hovertext
    # figure = dict(data=[Scatter()], layout=layout)

    return figure

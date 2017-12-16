import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd



# Add data
def chart_words(first,second):

    if first=="good":
        top_n ='positive nouns'
        top_c = 'rgb(22, 96, 167)'
        bot_n = 'negative nouns'
        bot_c = 'rgb(205, 12, 24)'

        # Edit the layout
        layout = dict(title = 'Top Positive Words Benchmarked Against Negative Frequency',
                      xaxis = dict(title = 'Words'),
                      yaxis = dict(title = 'Frequency'),
                      )
    if first == "bad":
        bot_n ='positive nouns'
        bot_c = 'rgb(22, 96, 167)'
        top_n = 'negative nouns'
        top_c = 'rgb(205, 12, 24)'

        # Edit the layout
        layout = dict(title='Top Negative Words Benchmarked Against Positive Frequency',
                      xaxis=dict(title='Words'),
                      yaxis=dict(title='Frequency'),
                      )



    ras = pd.read_csv(first + "_" +second+".csv")

    month = list(ras["name"].values)

    good = list(ras["good"].values)
    bad = list(ras["bad"].values)

    # Create and style traces

    trace1 = go.Scatter(
        x = month,
        y = good,
        name = top_n,
        line = dict(
            color=(top_c),
            width = 4,
            dash = 'dash') # dash options include 'dash', 'dot', and 'dashdot'
    )

    trace2 = go.Scatter(
        x = month,
        y = bad,
        name = bot_n,
        line = dict(
            color=(bot_c),

            width = 4,
            dash = 'dash')
    )

    data = [trace1,trace2 ]


    fig = dict(data=data, layout=layout)
    return fig


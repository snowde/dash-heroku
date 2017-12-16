import numpy as np
import pandas as pd

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd


glassdoor = pd.read_csv("gdoor_employee_rate.csv")
glassdoor_m= pd.read_csv("gdoor_mgmt_rate.csv")
df_tick= pd.read_csv("stock_rate.csv")
yelp= pd.read_csv("cutomer_rate")




trace_emp = go.Scatter(
    x=glassdoor["Review Date"],
    y=glassdoor["Final_Rating"],
    name = "Employees Sentiment",
    line = dict(color = '#17BECF'),

    opacity = 0.8)

trace_wlb = go.Scatter(
    x=glassdoor["Review Date"],
    y=glassdoor["Final_Work Life Balance"],
    name = "Work Life Balance",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_cva = go.Scatter(
    x=glassdoor["Review Date"],
    y=glassdoor["Final_Culture Values"],
    name = "Culture Values",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_cop = go.Scatter(
    x=glassdoor["Review Date"],
    y=glassdoor["Final_Career Opportunities"],
    name = "Career Opportunities",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_cbe = go.Scatter(
    x=glassdoor["Review Date"],
    y=glassdoor["Final_Comp Benefits"],
    name = "Comp Benefits",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_sma = go.Scatter(
    x=glassdoor["Review Date"],
    y=glassdoor["Final_Senior Management"],
    name = "Management Likability",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_mse = go.Scatter(
    x=glassdoor_m["date"],
    y=glassdoor_m["trace_mse"],
    name = "Management Sentiment",
    line = dict(color = 'green'),
    opacity = 0.8)

###

trace_mwlb = go.Scatter(
    x=glassdoor_m["date"],
    y= glassdoor_m["trace_mwlb"],
    name = "Work Life Balance",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_mcva = go.Scatter(
    x=glassdoor_m["date"],
    y=glassdoor_m["trace_mcva"],
    name = "Culture Values",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_mcop = go.Scatter(
    x=glassdoor_m["date"],
    y=glassdoor_m["trace_mcop"],
    name = "Career Opportunities",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_mcbe = go.Scatter(
    x=glassdoor_m["date"],
    y=glassdoor_m["trace_mcbe"],
    name = "Comp Benefits",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

trace_msma = go.Scatter(
    x=glassdoor_m["date"],
    y=glassdoor_m["trace_msma"],
    name = "Management Likability",
    line = dict(color = '#17BECF'),
    legendgroup='Employees',
    opacity = 0.2)

###


trace_sto = go.Scatter(
    x=df_tick["date"],
    y=df_tick["close"],
    name = "Stock Price",
    line = dict(color = '#7F7F7F'),
    opacity = 1)

trace_cus = go.Scatter(
    x=yelp["date"],
    y=yelp["Final_Rating"],
    name = "Customer Sentiment",
    line = dict(color = "orange"),
    opacity = 0.8)

# Google Search #
search_df = pd.read_csv("searches_BRJI.csv")
rat = pd.read_csv("rat_search.csv")
search = []

import colorlover as cl

daf = ["red","green","blue","violet","purple","grey" ]

search_dandas = pd.read_csv("searches_BRJI_dandas.csv")


trace_search_all = go.Scatter(
    x=search_dandas["date"],
    y=search_dandas.sum(axis=1)/(len(search_dandas.columns)-1),
    name = "Search Sentiment",
    opacity = 0.8)

rit = -1
for col in search_dandas.drop(["date"], axis=1).columns:
    rit = rit + 1
    trace = go.Scatter(x=search_dandas["date"], y=search_dandas[col], line = dict(color = daf[rit]),name=col,legendgroup=col,  opacity=0.8)
    search.append(trace)
#print(rat)#

color_dict = {}
sam = -1
for i in ["Reds","Greens","Blues","PuRd","Purples","Greys" ]:
    sam = sam + 1
    dan = cl.flipper()['seq'][str(rat.groupby("type").count().max()[0]+1)][i]
    color_dict[sam] = dan



for col in search_df.drop(["date"],axis=1).columns:
    tio = -1
    for g in rat["type"].unique():
        tio = tio + 1
        ban = daf[tio]
        if col in rat[rat["type"]==g]["0"].values:
            trace = go.Scatter(x = search_df["date"], y=search_df[col],line = dict(color = ban), name = col,legendgroup=g,opacity = 0.05)
            search.append(trace)

dat = pd.read_csv("all_yelps_rates.csv")

yep = []

trace_all_yelp = go.Scatter(x = dat["date"], y=dat["all"],line = dict(color = 'orange'), name = "Customer Sentiment",legendgroup="yelps", opacity = 0.8)
yep.append(trace_all_yelp)
for col in dat.drop(["date","all"],axis=1).columns:
    trace = go.Scatter(x = dat["date"], y=dat[col],line = dict(color = 'orange'), name = col,legendgroup="yelps", opacity = 0.10)
    yep.append(trace)


df_rick = df_tick[df_tick["date"]<search_dandas["date"].max()]
trace_stock = go.Scatter(
    x=df_rick["date"],
    y=df_rick["close"],
    name = "Stock",
    line = dict(color = '#7F7F7F'),
    opacity = 1)

search.append(trace_stock)
yep.append(trace_sto)

# now do the api call####

data = [trace_sto,trace_emp, trace_mse, trace_all_yelp,trace_search_all]

layout = dict(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    ),
    hovermode="closest"
)

fig_overall = dict(data=data, layout=layout)
#py.iplot(fig, filename = "Time Series with Rangeslider")####

fig_search = dict(data=search, layout=layout)

emp_data = [trace_sto,trace_emp, trace_wlb, trace_cop, trace_cbe, trace_sma]

fig_emp = dict(data=emp_data, layout=layout)

mgm_data = [trace_sto, trace_mse, trace_mwlb, trace_mcop, trace_mcbe, trace_msma]

fig_mgm = dict(data=mgm_data, layout=layout)

#
share_data = [trace_sto]

fig_sha = dict(data=share_data, layout=layout)


fig_cus = dict(data=yep, layout=layout)

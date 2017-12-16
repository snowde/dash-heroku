import pandas as pd

pd.set_option('display.max_columns', None)
import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl
import numpy as np
from flask import Flask
import pickle


pd.set_option('display.max_columns', None)

import intrinio

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


def Standardisation(df):
    listed = list(df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    return df


def Normalisation(df):
    listed = list(df)
    index = df.index
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    df.index = index
    return df


import intrinio

intrinio.client.username = 'cae7d0c54c6e7fd5363fc315b7fc7a4a'
intrinio.client.password = '8dc75b7fcc16e0a4782b789785eb0241'

tick = ["BJRI", "CMG"]
drop = {}

for t in tick:
    import good_morning as gm

    kr = gm.KeyRatiosDownloader()
    kr_frames = kr.download(t)

    import good_morning as gm

    kr = gm.FinancialsDownloader()
    kr_fins = kr.download(t)

    for key in ['income_statement', 'balance_sheet', 'cash_flow']:
        ra = kr_fins[key].ix[:, 1:].set_index("title").T
        ra.index.names = ["year"]
        ra.columns.name = None

        ra.index = ra.index.to_series().astype(str).astype(int)

        kr_fins[key] = ra

    conc = pd.DataFrame()
    for value in kr_frames:
        conc = pd.concat((conc, value), axis=0)

    df = conc.replace("Period", "Year")

    df = df.T

    df.index.names = ["year"]

    df = df.reset_index()

    df.index.names = ["year"]

    df.columns.name = None

    df = df.set_index(["year"], drop=True)

    df.index = df.index.to_series().astype(str).astype(int)

    kr_fins["calculations"] = conc.T

    for key in ['income_statement', 'balance_sheet', 'cash_flow', 'calculations']:
        df = kr_fins[key]

        drop[t, key] = df

import pickle

f = open("finance_dict.pkl", "wb")
pickle.dump(drop, f)
f.close()

with open('finance_dict.pkl', 'rb') as handle:
    dict_fin = pickle.load(handle)

# for period in ["FY","QTR","TTM","YTD"]: For now I will just leave them out
statement = ["calculations", "income_statement","balance_sheet","cash_flow"]

def price_extract(ticker):

    price = intrinio.prices(ticker, start_date=2008, frequency="yearly", sort_order='asc')

    price.index = pd.to_datetime(price.index, format="%Y-%m-%d")
    price["year"] = pd.DatetimeIndex(price.index).year

    price = price[price.index > "2008-12-31"]

    price_norm = pd.concat((Normalisation(price.drop("year", axis=1)), price["year"]), axis=1)

    return price, price_norm


def data_extract(ticker, request):
    DARS_2 = dict_fin[ticker, request]

    DARS_1 = DARS_2.fillna(value=0.01)
    DARS_1 = DARS_1.replace(0, 0.01)

    DARS_N = DARS_1

    DARS_N.index = DARS_N.index.to_series().astype(str).astype(int)

    DARS_N = DARS_N[DARS_N.index.values > 2008]

    DARS_N = Normalisation(DARS_N)
    DARS_N = DARS_N.replace(0, 0.01)
    DARS_1 = DARS_1[DARS_1.index.values > 2008]

    DARS_N.reset_index(inplace=True)

    DARS_1.reset_index(inplace=True)

    org, nor = price_extract(ticker)

    DARS_N = pd.merge(DARS_N, nor[["adj_close", "year"]], on="year", how="left")
    DARS_1 = pd.merge(DARS_1, org[["adj_close", "year"]], on="year", how="left")

    return DARS_1, DARS_N


ticks = ["BJRI", "CMG"]
for ticker in ticks:
            for request in ["calculations", "income_statement", "balance_sheet", "cash_flow"]:
                # for request in ["calculations"]:
                original, normalised = data_extract(ticker, request)
                original.to_csv("org" + "_" + request + "_" + ticker + ".csv", index=False)
                normalised.to_csv("sta" + "_" + request + "_" + ticker + ".csv", index=False)
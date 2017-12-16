#####################
##Figure Processing##
#####################

import pandas as pd


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
    print(filename)

    with open(str(filename), "wb") as f:
        f.write(data)

    ff = pd.read_excel(filename)
    return ff


competitors_df = db_frame("https://www.dropbox.com/s/hbsz0uod7w5dsxl/competitors.xlsx?dl=0")

tick = "BJRI"
year = int(2012)

from pandas_datareader.google.daily import GoogleDailyReader
from datetime import datetime, timedelta


class FixedGoogleDailyReader(GoogleDailyReader):
    @property
    def url(self):
        return 'http://finance.google.com/finance/historical'


start = datetime(year, 1, 1)
end = datetime.now()
df_tick = pd.DataFrame(
    FixedGoogleDailyReader(tick, start=start, end=end, chunksize=25, retry_count=3, pause=0.001, session=None).read())
df_tick = df_tick.reset_index()
df_tick = df_tick.rename(
    columns={'Volume': 'volume', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open', 'Date': 'date'})

# bench = "MENU"

# df_bench = pd.DataFrame(FixedGoogleDailyReader(bench, start=start, end=end, chunksize=25, retry_count=3, pause=0.001, session=None).read())
# df_bench = df_bench.reset_index()
# df_bench = df_bench.rename(columns={'Volume':'volume','Close':'close', 'High':'high', 'Low':'low', 'Open':'open', 'Date':'date'})


from pandas_datareader.google.daily import GoogleDailyReader
from datetime import datetime, timedelta


class FixedGoogleDailyReader(GoogleDailyReader):
    @property
    def url(self):
        return 'http://finance.google.com/finance/historical'


df_tick["close"] = df_tick["close"] * 100 / df_tick["close"].iloc[0]


def comp_tick(comp_ticks, comp_weight, df_tick):
    df_final = pd.DataFrame(index=df_tick.index)
    df_final["close"] = 0
    df_frame = pd.DataFrame()

    for bench, weight in zip(comp_ticks, comp_weight):
        start = datetime(year, 1, 1)
        end = datetime.now()

        df_bench = pd.DataFrame(
            FixedGoogleDailyReader(bench, start=start, end=end, chunksize=25, retry_count=3, pause=0.001,
                                   session=None).read())
        df_bench = df_bench.reset_index()
        df_bench = df_bench.rename(
            columns={'Volume': 'volume', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Open': 'open',
                     'Date': 'date'})

        df_bench = pd.merge(df_tick[["date", "low"]], df_bench[["date", "close"]], how="left")
        df_bench["close"] = df_bench["close"].fillna(method="bfill")
        df_bench["close"] = df_bench["close"].fillna(method="ffill")
        df_bench["close"] = df_bench["close"].fillna(df_bench["close"].mean())
        df_bench["close"] = df_bench["close"].fillna(value=0)
        df_bench["close"] = df_bench["close"] * 100 / df_bench["close"].iloc[0]

        #     print(bench)
        #     print(df_bench.iloc[276])

        df_final["close"] = df_final["close"] + df_bench["close"] * float(weight)
        df_frame[str(bench)] = df_bench["close"]

    df_final["date"] = df_tick["date"]

    df_final["close"] = df_final["close"] * 100 / df_final["close"].iloc[0]

    df_final["date"] = pd.to_datetime(df_final["date"], format="%Y-%m-%d")


    return df_final, df_frame


df_final, df_frame = comp_tick(competitors_df["Ticker"], competitors_df["Weight"], df_tick)


corrs = df_frame.corr()[tick].sort_values(ascending=False)
five = corrs.ix[1:6].index.values

df_final_filt, _ = comp_tick(five, [1 / five.shape[0] for i in list(range(five.shape[0]))], df_tick)

import numpy as np

hack = np.array([five[0], five[0]])
df_final_one, _ = comp_tick(hack, [1 / hack.shape[0] for i in list(range(hack.shape[0]))], df_tick)

df_final_filt.to_csv("comp_f_df.csv")
df_final_one.to_csv("comp_o_df.csv")

df_final.to_csv("comp_df.csv")
df_tick.to_csv("tick_df.csv")

print("done")
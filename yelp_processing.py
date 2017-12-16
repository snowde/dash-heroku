
import pandas as pd


csv_file = pd.read_csv("BJRI_locations.csv")

full_names = []
small_names = []
for i in range(len(csv_file["Link"].iloc[:47])):
    my_string = csv_file["Link"][i]
    dra = my_string.split("biz/", 1)[1]
    full_names.append(dra)
    var = dra.split("brewhouse-", 1)[1]
    small_names.append(var)


def yelp_final(yelp):
    tak = len(yelp)

    yelp = yelp.sort_values("date", ascending=True)

    yelp["roll25"] = pd.rolling_mean(yelp["rating"], int(tak * 0.05) + 3)
    yelp["roll100"] = pd.rolling_mean(yelp["rating"], int(tak * 0.2))
    yelp["roll250"] = pd.rolling_mean(yelp["rating"], int(tak * 0.5))

    yelp["roll100"] = yelp["roll100"].fillna(yelp["roll25"])
    yelp["roll250"] = yelp["roll250"].fillna(yelp["roll100"])
    yelp["roll250"] = yelp["roll250"].fillna(yelp["roll25"])

    yelp = yelp.sort_values("date", ascending=False)

    yelp["special_25"] = pd.rolling_mean(yelp["rating"], int(tak * 0.05) + 3)

    yelp["special_25"] = yelp["special_25"] * .80 + yelp["rating"] * .10
    # Left 10% out here, that is okay I assume.

    yelp["roll100"] = yelp["roll100"].fillna(yelp["special_25"])
    yelp["roll25"] = yelp["roll25"].fillna(yelp["special_25"])
    yelp["roll250"] = yelp["roll250"].fillna(yelp["special_25"])

    yelp = yelp.sort_values("date", ascending=True)

    yelp["Final_Rating"] = yelp["roll25"] * .40 + yelp["roll100"] * .40 + yelp["roll100"] * .20

    # multiplier = df_tick["close"].tail(1).values[0]/yelp["Final_Rating"].tail(1).values[0]

    # yelp["Final_Rating"] = yelp["Final_Rating"] * multiplier
    # print(yelp["Final_Rating"].head())
    return yelp["Final_Rating"]


from datetime import datetime
from dateutil.parser import parse

df_tick = pd.read_csv("stock_rate.csv")

# Range input and related index
ras = pd.DataFrame()
beg = pd.Timestamp('2010-05-15')
end = pd.Timestamp('2017-12-15')
idx = pd.DatetimeIndex(start=beg, end=end, freq='D')

ras["date"] = idx

df_tick["date"] = pd.to_datetime(df_tick["date"])
r = -1
for i in full_names:
    r = r + 1
    yp = pd.read_csv("files/" + i + ".csv")
    small = small_names[r]
    yp["date"] = yp["date"].apply(lambda x: x[:10])
    yp["date"] = yp["date"].apply(lambda x: x[:-1] if x[-1] == "\\" else x)
    yp["date"] = yp["date"].apply(lambda x: x[:-2] if x[-1] == "n" else x)

    yp['date'] = yp['date'].apply(lambda x: parse(x))

    # yp["date"] = pd.to_datetime(yp["date"])
    yp[small] = yelp_final(yp)
    ras = pd.merge(ras, yp[[small, "date"]], on="date", how="left")

ras = ras.fillna(method="ffill")
ras = ras.fillna(method="bfill")
ras = ras.fillna(value=0)

ras["date"] = pd.to_datetime(ras["date"])
ras = ras[ras["date"] <= df_tick["date"].max()]
ras = ras[ras["date"] > "2012-06-01"]

ras["all"] = 0
fas = ras
fas["all"] = fas[fas.drop("date", axis=1).columns].sum(axis=1)
fas["all"] = fas["all"] / len(fas.drop("date", axis=1).columns)

fas.to_csv("all_yelps_rates.csv", index=False)
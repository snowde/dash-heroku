import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

glassdoor = pd.read_csv("gdoor_employee_rate.csv")
glassdoor["Final_Rating_Employee"] = glassdoor["Final_Rating"]
glassdoor_m = pd.read_csv("gdoor_mgmt_rate.csv")
glassdoor_m["Final_Rating_Management"] = glassdoor_m["trace_mse"]

df_tick = pd.read_csv("stock_rate.csv")
yelp = pd.read_csv("cutomer_rate")
yelp["Final_Rating_Customer"] = yelp["Final_Rating"]

# Range input and related index
ras = pd.DataFrame()
beg = pd.Timestamp('2010-05-15')
end = pd.Timestamp('2017-12-15')
idx = pd.DatetimeIndex(start=beg, end=end, freq='D')

ras["date"] = idx

glassdoor["Review Date"] = pd.to_datetime(glassdoor["Review Date"])
glassdoor_m["Review Date"] = pd.to_datetime(glassdoor_m["Review Date_y"])
df_tick["date"] = pd.to_datetime(df_tick["date"])
yelp["date"] = pd.to_datetime(yelp["date"])

kas = pd.merge(ras, glassdoor, left_on="date", right_on="Review Date", how="left")
kas = pd.merge(kas, glassdoor_m[["Review Date", "Final_Rating_Management"]], left_on="date", right_on="Review Date",
               how="left")
pas = pd.merge(kas, df_tick, on="date", how="left")
kas = pd.merge(pas, yelp, on="date", how="left")

kas = kas[kas["date"] > "2012-06-01"]

kas = kas.fillna(method="ffill")
kas = kas.fillna(method="bfill")
kas = kas.fillna(value=0)

new = kas[["date", "Final_Rating_Employee", "Final_Work Life Balance",
           "Final_Culture Values", "Final_Career Opportunities",
           "Final_Comp Benefits", "Final_Senior Management",
           "Final_Rating_Management", "close", "Final_Rating_Customer"]]


def Normalisation(df):
    listed = list(df)
    index = df.index
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    df.index = index
    return df


cors = pd.read_csv("import_corr_BJRI.csv").drop(
    ["hula mamas", "minecraft kitchen mod", "hecho sf", "cancer traits male"], axis=1)

cors["date"] = pd.to_datetime(cors["date"])

date = cors["date"]

cors = cors.sort_values("date", ascending=True)

rat = pd.DataFrame(cors.drop(["date"], axis=1).columns)

rat["type"] = np.array(
    ["travel", "travel", "cars", "food", "food", "food", "travel", "food", "travel", "cars", "food", "travel", "travel",
     "credit", "credit"])

dandas = pd.DataFrame()
for r in rat["type"].unique():
    dandas[r] = cors["date"]
    dandas[r] = 0

for r in rat["type"].unique():
    print(r)
    for i in rat[rat["type"] == r][0].unique():
        print(i)
        dandas[r] = dandas[r] + cors[i]

dandas = Normalisation(dandas) * 5
dandas = dandas.replace(0, 0.01)

multiplier = df_tick["close"].tail(1).values[0] / dandas.tail(1).values[0]

dandas = dandas * multiplier

dandas["date"] = date

dandas = dandas[dandas["date"] > "2012-01-01"]

dandas.reset_index(drop=True, inplace=True)

dandas.to_csv("searches_BRJI_dandas.csv", index=False)

cors = Normalisation(cors.drop("date", axis=1))
cors = cors.replace(0, 0.01)

multiplier = df_tick["close"].tail(1).values[0] / cors.tail(1).values[0]

#nrt = cors
nrt = cors * multiplier

nrt["date"] = date

nrt = nrt[nrt["date"] > "2012-01-01"]

nrt.reset_index(drop=True, inplace=True)

nrt.to_csv("searches_BRJI.csv", index=False)

rat.to_csv("rat_search.csv", index=False)
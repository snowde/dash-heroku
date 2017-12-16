import pandas as pd

import datetime
from six.moves import cPickle as pickle #for performance



s = [ "'"+str(int(str(datetime.datetime.now().year)[-2:])-4+i) for i in range(5)]


s_metrics_df = pd.DataFrame([["Type","E","C","S","M","A","BA"],
                             ["Rating",1,1,1,1,1,1],
                             ["Performance",2,1,1,1,1,1],
                             ["Sentiment",3,1,1,1,1,1],
                             ["Loyalty",4,1,1,1,1,1]])

c_metrics_df = pd.DataFrame([["Year",s[0],s[1],s[2],s[3],s[4]],
                             ["Solvency",1,1,1,1,1],
                             ["Efficiency",2,1,1,1,1],
                             ["Profitability",3,1,1,1,1],
                             ["Liquidity",4,1,1,1,1]])



# Function To Import Dictionary and Open IT.
def load_dict(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pd.read_pickle(f)
    return ret_di

# And the specification of this table
dict_frames = load_dict('./data.pkl') # Much rather use this one


def fin_met(coy,bench):

    df_input = dict_frames[coy, "calculations", "Original"].round(2)
    df_input_b = dict_frames[bench, "calculations", "Original"].round(2)

    ratios_df = pd.DataFrame([   ["",	'Yr 1',	'Yr 2',	'Yr 3',	'Yr5',	'Yr1',	'Yr2',	'Yr3',	'Yr5'],
                                 ['Revenue growth',	df_input["Year over Year"].iloc[-1],	df_input["Year over Year"].iloc[-2],	df_input["Year over Year"].iloc[-3],	df_input["Year over Year"].iloc[-5],df_input_b["Year over Year"].iloc[-1],	df_input_b["Year over Year"].iloc[-2],df_input_b["Year over Year"].iloc[-3],	df_input_b["Year over Year"].iloc[-5]],
                                 ['EPS growth',	df_input["Year over Year.3"].iloc[-1],	df_input["Year over Year.3"].iloc[-2],	df_input["Year over Year.3"].iloc[-3],	df_input["Year over Year.3"].iloc[-5],df_input_b["Year over Year.3"].iloc[-1],	df_input_b["Year over Year.3"].iloc[-2],df_input_b["Year over Year.3"].iloc[-3],	df_input_b["Year over Year.3"].iloc[-5]],
                                 ['EV/EBITDA',	df_input["COGS"].iloc[-1],	df_input["COGS"].iloc[-2],	df_input["COGS"].iloc[-3],	df_input["COGS"].iloc[-5],df_input_b["COGS"].iloc[-1],	df_input_b["COGS"].iloc[-2],df_input_b["COGS"].iloc[-3],	df_input_b["COGS"].iloc[-5]],
                                 ['PE',	df_input["COGS"].iloc[-1],	df_input["COGS"].iloc[-2],	df_input["COGS"].iloc[-3],	df_input["COGS"].iloc[-5],df_input_b["COGS"].iloc[-1],	df_input_b["COGS"].iloc[-2],df_input_b["COGS"].iloc[-3],	df_input_b["COGS"].iloc[-5]],
                                 ['ROA',	df_input["Return on Assets %"].iloc[-1],	df_input["Return on Assets %"].iloc[-2],	df_input["Return on Assets %"].iloc[-3],	df_input["Return on Assets %"].iloc[-5],df_input_b["Return on Assets %"].iloc[-1],	df_input_b["Return on Assets %"].iloc[-2],df_input_b["Return on Assets %"].iloc[-3],	df_input_b["Return on Assets %"].iloc[-5]],
                                 ['Interest Cover EBIT',	df_input["Interest Coverage"].iloc[-1],	df_input["Interest Coverage"].iloc[-2],	df_input["Interest Coverage"].iloc[-3],	df_input["Interest Coverage"].iloc[-5],df_input_b["Interest Coverage"].iloc[-1],	df_input_b["Interest Coverage"].iloc[-2],df_input_b["Interest Coverage"].iloc[-3],	df_input_b["Interest Coverage"].iloc[-5]]])

    return ratios_df

c_metrics_df_2 = c_metrics_df.set_index(0,drop=True)


new_open_string = "{BJ's}  {}."























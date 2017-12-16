# Library Packages
import regex as re
import itertools as it
import spacy

% run
libraries.py
from __future__ import division

# Settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
seed = 7
np.random.seed(seed)

import warnings

warnings.filterwarnings('ignore')


def front(self, n):
    return self.iloc[:, :n]


def back(self, n):
    return self.iloc[:, -n:]


# Like normalization, standardization can be useful, and even required in some
# machine learning algorithms when your time series data has input values with differing scales.

from sklearn.preprocessing import StandardScaler


def Standardisation(df):
    listed = list(df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    return df


np.set_printoptions(threshold=np.nan)

!free - h#

yelp = pd.read_csv("bjs-restaurant-sanbruno.csv")

yelp["date"] = yelp["date"].apply(lambda x: x[:10])
yelp["date"] = yelp["date"].apply(lambda x: x[:-1] if x[-1] == "\\" else x)
yelp["date"] = yelp["date"].apply(lambda x: x[:-2] if x[-1] == "n" else x)

from datetime import datetime
from dateutil.parser import parse

yelp['date'] = yelp['date'].apply(lambda x: parse(x))

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

yelp["positive"] = 0
yelp["compound"] = 0.0
yelp["negative"] = 0
yelp["neutral"] = 0

analyzer = SIA()
for sentence, row in zip(yelp["review"], list(range(yelp.shape[0]))):
    vs = analyzer.polarity_scores(sentence)
    yelp["compound"][row] = float(vs["compound"])
    if vs["compound"] < -0.5:
        yelp["negative"][row] = 1
    elif vs["compound"] > 0.5:
        yelp["positive"][row] = 1
    else:
        yelp["neutral"][row] = 1
        # print("{:-<65} {}".format(sentence, str(vs)))

worst = yelp[(yelp["rating"] == 1) & (yelp["compound"] < -.95)]
worst = worst.sort_values("date", ascending=False).head(10).reset_index()

best = yelp[(yelp["rating"] == 5) & (yelp["compound"] > .95)]
best = best.sort_values("date", ascending=False).head(10).reset_index()

# Entity Extraction From Review
import itertools as it
import spacy

nlp = spacy.load('en')

sample_review = ""
for i in best["review"]:
    sample_review = sample_review + str(i)

# print(sample_review)

len(sample_review)

sample_review = sample_review.replace("\\", "")

parsed_review = nlp(sample_review)

# print(parsed_review)

token_text = [token.orth_ for token in parsed_review]
token_pos = [token.pos_ for token in parsed_review]

df = pd.DataFrame({'token_text': token_text, 'part_of_speech': token_pos})

# Unigrams
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

token = nltk.word_tokenize(str(parsed_review))
grams = ngrams(token, 1)

dra = Counter(grams)

t = pd.DataFrame()
f = pd.DataFrame(list(dra.keys()))

f = f[0]

t["name"] = f
t["count"] = list(dra.values())

df = df.drop_duplicates()
r = pd.merge(t, df, left_on=["name"], right_on=["token_text"], how="left", right_index=False)
r = r.drop("token_text", axis=1)
r.columns = ["name", "count", "pos"]

# Entity Extraction From Review
import itertools as it
import spacy


def g_o_b(type_df):
    nlp = spacy.load('en')

    sample_review = ""
    for i in type_df["review"]:
        sample_review = sample_review + str(i)

    # print(sample_review)

    len(sample_review)

    sample_review = sample_review.replace("\\", "")

    parsed_review = nlp(sample_review)

    # print(parsed_review)

    token_text = [token.orth_ for token in parsed_review]
    token_pos = [token.pos_ for token in parsed_review]

    df = pd.DataFrame({'token_text': token_text, 'part_of_speech': token_pos})

    # Unigrams
    import nltk
    from nltk import word_tokenize
    from nltk.util import ngrams
    from collections import Counter

    token = nltk.word_tokenize(str(parsed_review))
    grams = ngrams(token, 1)

    dra = Counter(grams)

    t = pd.DataFrame()
    f = pd.DataFrame(list(dra.keys()))

    f = f[0]

    t["name"] = f
    t["count"] = list(dra.values())

    df = df.drop_duplicates()
    r = pd.merge(t, df, left_on=["name"], right_on=["token_text"], how="left", right_index=False)
    r = r.drop("token_text", axis=1)
    r.columns = ["name", "count", "pos"]

    dfs = r[r["pos"] == "NOUN"].sort_values("count", ascending=False)
    return dfs


def firstme(first, second, tex1, tex2):
    ras = g_o_b(first).head(10)
    vas = g_o_b(second)

    vas = vas[vas.name.isin(list(ras["name"].values))].sort_values("count", ascending=False).head(10)

    kas = pd.merge(ras, vas, on="name", how="left")

    kas.fillna(value=0, inplace=True)
    kas.columns = ["name", tex1, "da", tex2, "da2"]
    kas.drop(["da", "da2"], axis=1)
    return kas


def gobp(type_df):
    nlp = spacy.load('en')

    sample_review = ""
    for i in type_df["review"]:
        sample_review = sample_review + str(i)

    # print(sample_review)

    len(sample_review)

    sample_review = sample_review.replace("\\", "")

    parsed_review = nlp(sample_review)

    ent = []
    lab = []

    for num, entity in enumerate(parsed_review.ents):
        ent.append(entity[0])
        lab.append(entity.label_)

    ent_df = pd.DataFrame()
    ent_df["entity"] = ent
    ent_df["label"] = lab
    rab = ent_df
    # for num, entity in enumerate(parsed_review.ents):
    #     ent_df["entity"][num] = entity
    #     ent_df["label"][num] = entity.label_


    ent_df["entity"] = ent_df["entity"].astype(str)

    ent_df = pd.merge(ent_df.groupby("entity").count().reset_index(), ent_df.drop_duplicates("entity"), on="entity",
                      how="left")

    ent_df.columns = ["entity", "count", "type"]

    from difflib import SequenceMatcher

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    vent = ent_df[ent_df["type"].isin(["GPE", "PERSON", "ORG"])]["entity"]

    import jellyfish
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process

    dar = []
    sar = []
    kar = []
    jar = []
    lev = []

    for i in vent:
        for r in vent:
            dar.append(i)
            sar.append(r)
            jar.append(jellyfish.jaro_distance(i, r))
            kar.append(similar(i, r))
            lev.append(jellyfish.levenshtein_distance(i, r))

    sos = pd.DataFrame()
    sos["original"] = dar
    sos["match"] = sar
    sos["percentage"] = kar
    sos["distance"] = jar
    sos["leven"] = lev
    sos["together"] = (sos["percentage"] + (sos["distance"]) / 2) * (1 / sos["leven"])
    # Including leven is important because it also counts the number
    # of characters, maybe change below, 0.2 to 0.3 if further issues.

    sos = sos[(sos["together"] < 1.0) & (sos["together"] > 0.4)].reset_index()

    sos["count_original"] = 0
    sos["count_contender"] = 0
    for i, c, r in zip(sos["original"], sos["match"], list(range(sos.shape[0]))):
        da = np.where(ent_df["entity"] == i, ent_df["count"], np.nan)
        x = da[~np.isnan(da)]
        sos["count_original"][r] = x

        da = np.where(ent_df["entity"] == c, ent_df["count"], np.nan)
        x = da[~np.isnan(da)]
        sos["count_contender"][r] = x

    sos

    dar = np.where(sos["count_original"] >= sos["count_contender"], sos["original"], sos["match"])
    sos["final"] = dar

    cas = sos[["match", "final"]]

    for match, final in zip(cas["match"], cas["final"]):
        print(match)
        ent_df['entity'] = ent_df.entity.replace([str(match)], [str(final)])

    res = pd.DataFrame()
    res["start"] = sos["original"]

    ent_df = pd.merge(ent_df.groupby("entity").sum().reset_index(),
                      ent_df.sort_values(["entity", "count"], ascending=["False", "False"]).drop_duplicates("entity",
                                                                                                            keep="first"),
                      on="entity", how="left")

    ent_df["count"] = ent_df["count_x"]

    ent_df = ent_df[["entity", "count", "type"]].sort_values("count", ascending=False)

    ent_df = ent_df[ent_df["type"].isin(["ORG", "PERSON", "GPE"])]
    # If a person uses the word twice, there is probably a good reasons, so done in that way.
    return ent_df


def firstme(first, second, tex1, tex2):
    ras = g_o_b(first).head(10)
    vas = g_o_b(second)

    vas = vas[vas.name.isin(list(ras["name"].values))].sort_values("count", ascending=False).head(10)

    kas = pd.merge(ras, vas, on="name", how="left")

    kas.fillna(value=0, inplace=True)
    kas.columns = ["name", tex1, "da", tex2, "da2"]
    kas.drop(["da", "da2"], axis=1)
    return kas


def firstmep(first, second, tex1, tex2):
    ras = gobp(first)
    ras = ras[~ras["entity"].isnull()]
    ras = ras[~ras["entity"].isin([" "])]
    vas = gobp(second)
    vas = vas[~vas["entity"].isnull()]
    vas = vas[~vas["entity"].isin([" "])]

    vas = vas[vas.entity.isin(list(ras["entity"].values))].sort_values("count", ascending=False).head(10)

    kas = pd.merge(ras, vas, on="entity", how="left")

    kas.fillna(value=0, inplace=True)
    kas.columns = ["entity", tex1, "da", tex2, "da2"]
    kas.drop(["da", "da2"], axis=1)
    return kas


# Normal Nouns Functions
kas = firstme(best, worst, "good", "bad")
kas.to_csv("good_bad.csv", index=False)

kas = firstme(worst, best, "bad", "good")
kas.to_csv("bad_good.csv", index=False)

# Pronoun Functions
guud_p = firstmep(best, worst, "best", "worst")

guud_p.to_csv("good_bad_pro.csv", index=False)

beet_p = firstmep(worst, best, "worst", "best")

beet_p.to_csv("bad_good_pro.csv", index=False)
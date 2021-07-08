import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime

df_historical = pd.read_csv("data/spy.csv", index_col=0)
r1 = requests.get(f"https://stockanalysis.com/etf/spy/holdings")
s1 = (
    bs(r1.text, "html.parser")
    .find("table", {"class": "fullholdings"})
    .find("tbody")
)
tick, percent, shares = [], [], []
for idx, entry in enumerate(s1.findAll("tr"), 1):
    tick.append(entry.findAll("td")[1].text)
    percent.append(float(entry.findAll("td")[3].text.strip("%")))
    if idx >= 200:
        break
df = pd.DataFrame(data=[percent])
df.columns = tick
df.index = [datetime.datetime.now().strftime("%m/%d/%Y")]
df["SUM"] = df.sum(axis=1)

new_df = pd.concat([df_historical, df], axis=0).fillna(0)
# Make SUM the last column
ordered_cols = list(new_df.columns)
ordered_cols.remove("SUM")
ordered_cols += ["SUM"]
new_df = new_df[[ordered_cols]]
new_df.to_csv("data/spy.csv")


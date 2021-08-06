import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime
import os
import random 

etf_symbols = []
data=requests.get("https://stockanalysis.com/_next/data/VDLj2l5sT7aRmdOwKVFT4/etf.json").json()
for entry in data["pageProps"]["stocks"]:
    etf_symbols.append(entry["s"])
    
# Not sure if some dont update due to times.  Add shuffle to randomly loop.
random.shuffle(etf_symbols)
# This ensures that at least spy and qqq runs first
etf_symbols.remove("SPY")
etf_symbols.remove("QQQ")
etf_symbols.insert(0, "QQQ")
etf_symbols.insert(0, "SPY")

for etf in etf_symbols:
    try:
        file = f"data/{etf}.csv"
        r1 = requests.get(f"https://stockanalysis.com/etf/{etf}/holdings")
        s1 = (
            bs(r1.text, "html.parser")
            .find("table", {"class": "fullholdings"})
            .find("tbody")
        )
        tick, percent, shares = [], [], []
        for idx, entry in enumerate(s1.findAll("tr"), 1):
            if entry.findAll("td")[1].text == "n/a":
                tick.append(entry.findAll("td")[2].text)
            else:
                tick.append(entry.findAll("td")[1].text)
            percent.append(
                float(entry.findAll("td")[3].text.strip("%").replace(",", "_"))
            )
            if idx >= 200:
                break
        df = pd.DataFrame(data=[percent])
        df.columns = tick
        df.index = [datetime.datetime.now().strftime("%m/%d/%Y")]
        df["SUM"] = df.sum(axis=1)
        if df.columns.value_counts().max() > 1:
            # Seems to occur for me with symbol 1117.hk having many desciptions as an example
            print("Too many entries")
            print(etf)
            continue

        try:
            df_historical = pd.read_csv(file, index_col=0)
            new_df = pd.concat([df_historical, df], axis=0).fillna(0)
        except FileNotFoundError:
            new_df = df.copy()
        # Make SUM the last column
        ordered_cols = list(new_df.columns)
        ordered_cols.remove("SUM")
        ordered_cols += ["SUM"]
        new_df = new_df[ordered_cols]
        new_df.to_csv(file)
    except Exception as e:
        print("error")
        print(etf)
        pass

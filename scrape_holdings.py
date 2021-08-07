import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime
import os
import random

r = requests.get("https://api.stockanalysis.com/etf/")
soup = bs(r.text, "html.parser").findAll("ul", {"class": "no-spacing"})
all_links = soup[0].findAll("li")
etf_symbols = []
etf_names = []
for link in all_links:
    etf_symbols.append(link.text.split("-")[0].strip(" "))
    etf_names.append(link.text.split("-")[1][1:])

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
        link = f"https://api.stockanalysis.com/etf/{etf}/holdings/"
        r = requests.get(link)
        soup = bs(r.text, "html.parser")
        soup = soup.find("table")
        tds = soup.findAll("td")
        tickers = []
        for i in tds[1::5]:
            tickers.append(i.text)
        percents = []
        for i in tds[3::5]:
            percents.append(float(i.text.strip("%")))
        df = pd.DataFrame(data=[percents])
        df.columns = tickers
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

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime
import os

r = requests.get("https://stockanalysis.com/etf/")
soup = bs(r.text, "html.parser").findAll("ul", {"class": "no-spacing"})
all_links = soup[0].findAll("li")
etf_symbols = []

for link in all_links:
    etf_symbols.append(link.text.split("-")[0].strip(" "))

for etf in etf_symbols:
    file = f"data/{etf}.csv"
    try:
        if os.path.exists(file):
            df_historical = pd.read_csv(file, index_col=0)
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
            percent.append(float(entry.findAll("td")[3].text.strip("%")))
            if idx >= 200:
                break
        df = pd.DataFrame(data=[percent])
        df.columns = tick
        df.index = [datetime.datetime.now().strftime("%m/%d/%Y")]
        df["SUM"] = df.sum(axis=1)
        if os.path.exists(file):
            new_df = pd.concat([df_historical, df], axis=0).fillna(0)
            # Make SUM the last column
            ordered_cols = list(new_df.columns)
            ordered_cols.remove("SUM")
            ordered_cols += ["SUM"]
            new_df = new_df[[ordered_cols]]

        else:
            new_df = df.copy()
        new_df.to_csv(file)
    except Exception as e:
        print(e)
        print(etf)
print(new_df)

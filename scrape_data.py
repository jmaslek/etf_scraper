import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import numpy as np

def assets_to_num(x):
    x = x.strip("$")
    if x.endswith("M"):
        return float(x.strip("M"))
    elif x.endswith("B"):
        return float(x.strip("B"))*1000
    elif x.endswith("K"):
        return float(x.strip("K"))/1000
    else:
        return np.nan

r = requests.get("https://stockanalysis.com/etf/")
soup = bs(r.text, "html.parser").findAll("ul", {"class": "no-spacing"})
all_links = soup[0].findAll("li")
etf_symbols = []

for link in all_links:
    etf_symbols.append(link.text.split("-")[0].strip(" "))

df = pd.DataFrame(columns = etf_symbols)
for etf in small_etfs:
    r1 = requests.get(f"https://stockanalysis.com/etf/{etf}")
    soup1 = bs(r1.text, "html.parser").find("div", {"class": "info"}).findAll("td")
    column = []
    value = []
    column.append("Last Price")
    value.append(
        bs(r1.text, "html.parser")
        .find("div", {"class": "quote"})
        .find("td", {"id": "qLast"})
        .text
    )
    for row in soup1[:-4:2]:
        column.append(row.text)
    for row in soup1[1:-4:2]:
        value.append(row.text)
    df[etf] = value
df.index = column
df = df.T
df.columns = ["Price", "Assets", "NAV", "Expense", "PE", "Beta", "Div", "DivYield"]
df["Price"] = df["Price"].apply(lambda x: float(x.strip("$")))
df["NAV"] = df["NAV"].apply(lambda x: float(x.strip("$")) if x != "n/a" else np.nan)
df["Expense"] = df["Expense"].apply(lambda x: float(x.strip("%")) if x != "n/a" else np.nan)
df["Div"] = df["Div"].apply(lambda x: float(x.strip("$")) if x != "n/a" else np.nan)
df["DivYield"] = df["DivYield"].apply(lambda x: float(x.strip("%")) if x != "n/a" else np.nan)
df["PE"] = df["PE"].apply(lambda x: float(x) if x != "n/a" else np.nan)
df["Beta"] = df["Beta"].apply(lambda x: float(x) if x != "n/a" else np.nan)
df["Assets"] = df["Assets"].apply(lambda x: assets_to_num(x))

df.to_csv("etf_overviews.csv")

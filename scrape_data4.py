import requests
import pandas as pd
import json
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
import numpy as np
import time
from requests.adapters import HTTPAdapter, Retry


def assets_to_num(x):
    x = x.strip("$")
    if x[-1] not in ["M","B","K"]:
        return x
    if x.endswith("M"):
        return float(x.strip("M"))
    elif x.endswith("B"):
        return float(x.strip("B")) * 1000
    elif x.endswith("K"):
        return float(x.strip("K")) / 1000
    else:
        return np.nan
    
s = requests.Session()

retries = Retry(total=10,
                backoff_factor=.5,
                status_forcelist=[ 429 ])

s.mount('https://', HTTPAdapter(max_retries=retries))
    
    
r = requests.get("https://stockanalysis.com/etf/", headers={"User-Agent":"Mozilla/5.0"})
soup2 = BeautifulSoup(r.text,"html.parser")
script = soup2.find("script",{"id":"__NEXT_DATA__"})
a1 = json.loads(soup2.find_all("script")[4].string)[1]
etf_symbols = pd.DataFrame(a1["data"]).s.to_list()
    
df = pd.read_csv("etf_overviews.csv", index_col=0).T
df = df.astype(str)
for etf in etf_symbols[1500:2000]:
    try:
        #r = requests.get(f"https://stockanalysis.com/etf/{etf}", headers={"User-Agent":"Mozilla/5.0"})
        r = s.get(f"https://stockanalysis.com/etf/{etf}", headers={"User-Agent":"Mozilla/5.0"})
        soup = bs(r.text, "html.parser")  # %%
        tables = soup.findAll("table")
        texts = []
        for tab in tables[:2]:
            entries = tab.findAll("td")
            for ent in entries:
                texts.append(ent.get_text())

        vars = [0, 2, 4, 6, 8, 10, 12, 18, 20, 22, 26, 28, 30, 32]
        vals = [idx + 1 for idx in vars]
        columns = [texts[idx] for idx in vars]
        data = [texts[idx] for idx in vals]    
        df[etf] = data
    except Exception as e:
        print(f"{etf}, status code: {r.status_code}")
        
df.index = columns
df = df.T
df.columns = ['Assets',
 'NAV',
 'Expense',
 'PE',
 'SharesOut',
 'Div',
 'DivYield',
 'Volume',
 'Open',
 'PrevClose',
 'YrLow',
 'YrHigh',
 'Beta',
 'N_Hold']

df["Assets"] = df["Assets"].apply(lambda x: assets_to_num(x) if isinstance(x,str) else np.nan)
df["NAV"] = df["NAV"].apply(lambda x: float(x.strip("$")) if x not in ["n/a","-"] else np.nan)
df["Expense"] = df["Expense"].apply(lambda x: float(x.strip("%")) if x not in ["n/a","-"] else np.nan)
df["PE"] = df["PE"].apply(lambda x: float(x) if x not in ["n/a","-"] else np.nan)
df["SharesOut"] = df["SharesOut"].apply(lambda x: assets_to_num(x))
df["Div"] = df["Div"].apply(lambda x: float(x.strip("$")) if x not in ["n/a","-"] else np.nan)
df["DivYield"] = df["DivYield"].apply(lambda x: float(x.strip("%").replace(",","")) if x not in ["n/a","-"] else np.nan)
df["Volume"] = df["Volume"].apply(lambda x: float(x.replace(",","")) if x not in ["n/a","-"] else np.nan)
df["PrevClose"] = df["PrevClose"].apply(lambda x: float(x.strip("$")) if x not in ["n/a","-"] else np.nan)
df["Open"] = df["Open"].apply(lambda x: float(x.strip("$")) if x not in ["n/a","-"] else np.nan)
df["PrevClose"] = df["PrevClose"].apply(lambda x: float(x) if x not in ["n/a","-"] else np.nan)
df["YrLow"] = df["YrLow"].apply(lambda x: float(x) if x not in ["n/a","-"] else np.nan)
df["YrHigh"] = df["YrHigh"].apply(lambda x: float(x) if x not in ["n/a","-"] else np.nan)
df["Beta"] = df["Beta"].apply(lambda x: float(x) if x not in ["n/a","-"] else np.nan)
df["N_Hold"] = df["N_Hold"].apply(lambda x: float(x) if x not in ["n/a","-"] else np.nan)

df.to_csv("etf_overviews.csv")

# etf_screener

This repo is a tool that scrapes etf data from [stockanalysis.com](stockanalysis.com).

Currently there are two scripts
- scrape_data.py
- scrape_holdings.py

These are currently set to both run at Midnight EST.  

## Scrape_data

This scrapes all avalaible ETFS and returns, Price, Total Assets (in Millions USD), Net Asset Value (NAV), Expense Ratio, PE Ratio, the 5 Year Beta, the dividend and the dividend yield.  Any data not available is reported as a NaN value. Data is saved in "etf_overviews.csv".

## Scrape_holdings

This scrapes the site for the top 200 Holdings in the given etf.  It runs every day at midnight as well.  As of today (7/8/21), I only look at SPY, so all etfs are on the TODO.  The index represents the date and the values are given in terms of percent.  The "SUM" column represents the total sum of the top 200.  An example is that on 7/7/21, the SUM for spy is 83.5, meaning there are more than 200 holdings, and teh rest account for the other 16.5 %.  Data is saved in the data folder ("data/etf_name.csv").

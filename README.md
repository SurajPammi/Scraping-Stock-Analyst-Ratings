# Scraping-Stock-Analyst-Ratings
Written in Python.

This purpose of this program is to scrape analyst ratings of a stock and displays the data using plotly.
Analyst ratings can be used in trading strategies.

Websites used for scraping using BeautifulSoup:
- swingtradebot.com
- zacks.com
- wsj.com 

Websites used for scraping using selenium (since BeautifulSoup was unable to scrape on these sites)
- Thestreet.com  
- tradingview.com 

Pandas data frame was used to hold analyst ratings and the website names. The data frame was then used for pie charts that was powered by plotly. There is a pie chart for each site and a pie chart for all ratings combined. 

## Dependencies
- bs4
- requests
- yfinance
- pandas
- selenium
- time
- plotly
``` python
from bs4 import BeautifulSoup as bs  # To parse HTML
import requests  # To open links
import yfinance as yf  # Check if the ticker entered is valid, also grabs the ticker's exchange (NYSE, NASDAQ, etc)
import pandas as pd  # Used for a data frame table to hold ratings, and analysts
import selenium.common
from selenium import webdriver  # To scrape JavaScript, used for Tradingview.com and TheStreet.com
import time  # Testing time it takes for scraping
from plotly.subplots import make_subplots # making multiple charts
import plotly.graph_objects as go # making a chart
```

## Demo
![](Analyst Rating GIF Demo Original.gif)

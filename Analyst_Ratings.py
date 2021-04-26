"""
***************************************************************************************************************
# Project: Stock Analyst Ratings Scrapper
# Date: 12-23-2020
# File: Analyst_Ratings.py
# File Description: Scrapes ratings from multiple websites and makes a pandas dataframe from the scrapped data
***************************************************************************************************************

"""

from bs4 import BeautifulSoup as bs  # To parse HTML
import requests  # To open links
import yfinance as yf  # Check if the ticker entered is valid, also grabs the ticker's exchange (NYSE, NASDAQ, etc)
import pandas as pd  # Used for a data frame table to hold ratings, and analysts
import selenium.common
from selenium import webdriver  # To scrape JavaScript, used for Tradingview.com and TheStreet.com
import time  # Testing time it takes for scraping


# * Global Constants Start * #
# Arguments for options parameter in selenium, used for efficiency boost
SELENIUM_ARGUMENT_EFFICIENCY = ["--headless", "disable-infobars", "--disable-extensions", '--no-sandbox',
                                '--no-default-browser-check', '--disable-gpu', '--disable-default-apps',
                                '--disable-dev-shm-usage']

# Ratings
COLUMNS = ["Strong Sell", "Sell", "Hold", "Buy", "Strong Buy"]
# * Global Constants End * #


# Function to verify that the ticker exists.
# Returns ticker and the exchange it belongs to
def verify_ticker():
    start_time = time.time()
    ticker = input(str("Ticker: "))
    while True:
        # Remove any spaces the user enters
        ticker = ticker.replace(" ", "")
        # Uses yahoo finance to validate
        api_ticker = yf.Ticker(ticker)
        try:
            exchange = api_ticker.info["exchange"]
        except KeyError:
            ticker = input(str("Ticker: "))
        else:
            end_time = time.time()
            print("Verify Object Time:", end_time - start_time)
            return ticker, str(make_exchange(exchange))


# Makes a soup object from link using requests to open the link
def soup_object(link):
    # header parameter needed so websites do not think this is a bot
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/56.0.2924.87 Safari/537.36 '

    try:
        requested_source = requests.get(link, headers=headers).text
    except requests.HTTPError as exception:
        print(exception)
        soup = None
        return soup

    soup = bs(requested_source, "lxml")
    return soup


# Gets Zacks rating based on ticker
def zacks_rating(ticker):
    time_start = time.time()

    zacks_link = "https://www.zacks.com/stock/quote/" + str(ticker) + "?q=" + str(ticker)
    soup = soup_object(zacks_link)
    if soup is None:
        return False
    line = soup.find(class_="rank_view")
    if line is None:
        return False
    line = line.text
    line = line.strip()
    # Currently, line = an integer from 1 to 5"-"rating" of 5    " first integer. Ex: line = 3-Hold of 5     3
    # Remove non alphabetical values
    line = (''.join([i for i in line if i.isalpha()]))
    line = line[:-2:]
    if not line:
        return False
    rating = line

    time_end = time.time()
    print("Zacks Time:", time_end - time_start)
    return rating


# Gets Swingtradebot rating based on ticker
def swingtradebot_rating(ticker):
    time_start = time.time()

    stb_link = "https://swingtradebot.com/equities/" + str(ticker)
    soup = soup_object(stb_link)
    # Finds where stb has its ranking on their page
    line = str(soup.find("td", class_="text-center"))
    if line is None:
        return False
    # Rating exists in this spot in the string
    rating = line[40]
    rating = change_rating_format(rating)
    time_end = time.time()
    print("SwingTradeBot Time:", time_end - time_start)
    return rating


# Initializes selenium webdriver
def initialize_selenium(link):
    options = webdriver.ChromeOptions()

    for i in range(len(SELENIUM_ARGUMENT_EFFICIENCY)):
        options.add_argument(SELENIUM_ARGUMENT_EFFICIENCY[i])
    # preferences for browser, 2 = block, 1 = accept
    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.default_content_setting_values.notifications": 2,
             "profile.managed_default_content_settings.stylesheets": 2,
             "profile.managed_default_content_settings.cookies": 2,
             "profile.managed_default_content_settings.javascript": 1,
             "profile.managed_default_content_settings.plugins": 2,
             "profile.managed_default_content_settings.popups": 2,
             "profile.managed_default_content_settings.geolocation": 2,
             "profile.managed_default_content_settings.media_stream": 2,

             }
    options.add_experimental_option("prefs", prefs)
    try:
      driver = webdriver.Chrome("/Users/Suraj/Downloads/chromedriver", options=options)
    except selenium.common.exceptions.SessionNotCreatedException:
      return False
    driver.implicitly_wait(2)
    driver.get(link)

    return driver


# Gets TheStreet rating based on ticker
def thestreet_rating(ticker):
    # bs does not work on this site, needs to use selenium
    time_start = time.time()
    ts_link = "https://www.thestreet.com/quote/" + ticker
    driver = initialize_selenium(ts_link)
    if driver == False:
        return False
    # Rating format on TheStreet is a grade system: A+ or B, or C+, etc
    try:
        grade = driver.find_element_by_class_name("m-market-data-quant--grade")
    except selenium.common.exceptions.NoSuchElementException:
        return False
    ranking = grade.text
    ranking = change_rating_format(ranking)
    time_end = time.time()
    print("theStreet Time:", time_end - time_start)
    return ranking


# Get WSJ Ratings based on ticker
def wsj_ratings(ticker):
    time_start = time.time()

    wsj_link = "https://www.wsj.com/market-data/quotes/" + ticker + "/research-ratings"
    soup = soup_object(wsj_link)
    if soup is None:
        return [], []
    line = soup.find(class_="cr_analystRatings cr_data module")
    if line is None:
        return [], []
    line = line.find(class_="cr_dataTable")
    line = line.find("tbody")
    # List: Name, 3 months ago ratings, 1 month ago rating, current, repeat
    line = line.text.split()

    # Code below is for creating a keys list and a values (ratings) list so we only insert into the df where its needed
    # Its so whe don't enter in 0s in the df. This is to make plotly formatting more clean
    keys = []
    # Order: Strong Sell, Sell, Hold, Buy, Strong Buy
    ratings = [int(line[19]), int(line[15]), int(line[11]), int(line[7]), int(line[3])]
    # Appends Buy/Sell keyword to keys list so we know where to insert into df
    for i in range(len(ratings)):
        if ratings[i] != 0:
            keys.append(COLUMNS[i])
    # List of non zeroes
    ratings = [i for i in ratings if i != 0]
    time_end = time.time()
    print("WSJ Time:", time_end - time_start)
    return ratings, keys


# Get Tradingview rating based on ticker
def tradingview_rating(ticker, exchange):
    # bs does not work on this site, need selenium to access data
    time_start = time.time()

    tv_link = "https://www.tradingview.com/symbols/" + exchange + "-" + ticker.upper() + "/technicals/"
    driver = initialize_selenium(tv_link)
    if driver == False:
        return False
    try:
        line = driver.find_element_by_class_name("speedometerSignal-pyzN--tL")
    except selenium.common.exceptions.NoSuchElementException:
        return False
    # Currently line is all uppercase
    line = line.text.lower()
    # Replace lower case first letter to uppercase for the change_rating_format function
    line = line.replace(line[0], line[0].upper())
    rating = line
    time_end = time.time()
    rating = change_rating_format(rating)
    print("Tradingview Time:", time_end - time_start)
    return rating


# Takes in API values for an exchange and turns them into universal exchange values
def make_exchange(exchange):
    # NMS = NASDAQ
    # ASE = AMEX
    # NYQ = NYSE
    if exchange == "NMS":
        exchange = "NASDAQ"
    if exchange == "ASE":
        exchange = "AMEX"
    if exchange == "NYQ":
        exchange = "NYSE"
    return exchange


# Makes a pandas data frame
def df_maker():
    start_time = time.time()

    ticker, exchange = verify_ticker()

    indexes = ["Zacks", "SwingTradeBot", "TradingView", "TheStreet", "Wall St. Analysts (WSJ)", "Totals", "MTotals"]
    rating, keys = wsj_ratings(ticker)
    stb_rate = swingtradebot_rating(ticker)
    zacks_rate = zacks_rating(ticker)
    tradingview_rate = tradingview_rating(ticker, exchange)
    thestreet_rate = thestreet_rating(ticker)

    df = pd.DataFrame(None,
                      index=indexes,
                      columns=COLUMNS)
    if zacks_rate:
        df.loc["Zacks", zacks_rate] = 1
    if stb_rate:
        df.loc["SwingTradeBot", stb_rate] = 1
    if tradingview_rate:
        df.loc["TradingView", tradingview_rate] = 1
    if thestreet_rate:
        df.loc["TheStreet", thestreet_rate] = 1
    for i in (range(len(rating))):
        df.loc["Wall St. Analysts (WSJ)", keys[i]] = rating[i]
    df.loc["Totals"] = df.sum(axis=0)

    # MTotals row needed so plotly chart does not have formatting issues with 0s in the Totals column
    columns = []
    totals = df.loc["Totals"]
    keys = []
    # Only grab values that exist from the Totals row
    for i in range(len(COLUMNS)):
        if totals[i] != 0:
            columns.append(totals[i])
            keys.append(COLUMNS[i])

    for i in range(len(keys)):
        df.loc["MTotals", keys[i]] = columns[i]

    end_time = time.time()
    print("Total Scrape Time:", end_time - start_time)
    print(df)
    return df


# Take in parameter format and turns it into a Buy/Sell format
def change_rating_format(rating):
    # Turn ratings list into a format that will make it easier to insert into a pandas df
    # Uses first letter only for grade (A, B) format because the "+" would add more cases
    if rating[0] == "E" or rating[0] == "F":
        return "Strong Sell"
    if rating[0] == "D":
        return "Sell"
    if rating == "Neutral" or rating[0] == "C":
        return "Hold"
    if rating[0] == "B":
        return "Buy"
    if rating[0] == "A":
        return "Strong Buy"
    return rating


if __name__ == "__main__":
    df_maker()


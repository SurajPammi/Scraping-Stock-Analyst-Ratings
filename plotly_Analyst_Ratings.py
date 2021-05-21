"""
***************************************************************************************************************
# Project: Stock Analyst Ratings Scrapper
# Date: 12-23-2020
# File: plotly_Analyst_Ratings.py
# File Description: Takes pandas dataframe from Analyst_Ratings.py and turns it into pie charts using plotly
***************************************************************************************************************
"""

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from Analyst_Ratings import df_maker, COLUMNS


if __name__ == "__main__":
    df = df_maker()
    # grabs pandas df from Analyst_Ratings.py

    """""
    Color Scheme: Strong Sell - Dark Red 
                  Sell - Red 
                  Hold - Yellow 
                  Buy - Light Green
                  Strong Buy - Dark Green
    """
    color_scheme = ["darkred", "red", "yellow", "lightgreen", "darkgreen"]

    figure_totals = make_subplots(
        rows=2, cols=2,  # pie charts will be layered out in a 2x2 area, this format looks clean
    )
    # Total Analyst Ratings pie chart
    figure_totals.add_trace(go.Pie(values=df.loc["MTotals"],
                                   labels=COLUMNS,
                                   marker=dict(colors=color_scheme),
                                   domain=dict(x=[0, 0.49]),  # Puts the chart in the first half of the x-axis
                                   title="Total Analyst Ratings",
                                   titleposition="top center",
                                   titlefont=dict(size=25),
                                   textinfo="percent+value",
                                   showlegend=True
                                   ))
    # These loop/if are needed because if any row has no data, plotly will display the wrong data for the other charts
    # Wall St. Analysts (WSJ) Ratings
    for i in range(len(COLUMNS)):
        if isinstance(df.loc["Wall St. Analysts (WSJ)", COLUMNS[i]], int):
            figure_totals.add_trace(go.Pie(values=df.loc["Wall St. Analysts (WSJ)"],
                                           labels=COLUMNS,
                                           marker=dict(colors=color_scheme),
                                           domain=dict(x=[.55, 1]),  # Puts the chart in the second half of the x-axis
                                           title="Wall St. Analysts (WSJ)",
                                           titleposition="top center",
                                           titlefont=dict(size=25),
                                           textinfo="percent+value"
                                           ))
            break
    # SwingTradeBot Rating
    for i in range(len(COLUMNS)):
        if isinstance(df.loc["SwingTradeBot", COLUMNS[i]], int):
            figure_totals.add_trace(go.Pie(values=df.loc["SwingTradeBot"],
                                           labels=COLUMNS,
                                           marker=dict(colors=color_scheme),
                                           domain=dict(x=[.41, .5], y=[.50, 1]),
                                           # Puts the chart in the middle of the page
                                           title="SwingTradeBot",
                                           titleposition="top center",
                                           titlefont=dict(size=15),
                                           textinfo="percent+value"
                                           ))
            break
    # Zacks Rating
    for i in range(len(COLUMNS)):
        if isinstance(df.loc["Zacks", COLUMNS[i]], int):
            figure_totals.add_trace(go.Pie(values=df.loc["Zacks"],
                                           labels=COLUMNS,
                                           marker=dict(colors=color_scheme),
                                           domain=dict(x=[.41, .5], y=[0, .50]),
                                           # Puts the chart in the middle of the page
                                           title="Zacks",
                                           titleposition="top center",
                                           titlefont=dict(size=15),
                                           textinfo="percent+value"
                                           ))
            break
    # TradingView Rating
    for i in range(len(COLUMNS)):
        if isinstance(df.loc["TradingView", COLUMNS[i]], int):
            figure_totals.add_trace(go.Pie(values=df.loc["TradingView"],
                                           labels=COLUMNS,
                                           marker=dict(colors=color_scheme),
                                           domain=dict(x=[.51, .6], y=[0, .50]),
                                           # Puts the chart in the middle of the page
                                           title="Tradingview",
                                           titleposition="top center",
                                           titlefont=dict(size=15),
                                           textinfo="percent+value"
                                           ))
            break
    # TheStreet Rating
    for i in range(len(COLUMNS)):
        if isinstance(df.loc["TheStreet", COLUMNS[i]], int):
            figure_totals.add_trace(go.Pie(values=df.loc["TheStreet"],
                                           labels=COLUMNS,
                                           marker=dict(colors=color_scheme),
                                           domain=dict(x=[.51, .6], y=[.5, 1]),
                                           # Puts the chart in the middle of the page
                                           title="TheStreet",
                                           titleposition="top center",
                                           titlefont=dict(size=15),
                                           textinfo="percent+value"
                                           ))
            break

    figure_totals.update_layout(title_text="Analyst Ratings")
    figure_totals.show(renderer='chrome')

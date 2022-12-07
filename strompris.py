#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime

import altair as alt
import pandas as pd
import requests
import requests_cache
import json
from dataclasses import dataclass
from datetime import timedelta

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()


# task 5.1:

def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    arguments:
        date (datetime.date) : a date object
        location: (str) : location to get the data from

    return:
        dataframe : a dataframe with all prices from the given day
    """

    # Set day to today if not specified
    if date is None:
        date = datetime.date.today()

    # Specify day and month
    day = date.day
    month = date.month

    # Zero pad if not already
    if len(str(date.day)) == 1:
        day = "0"+str(date.day)

    if len(str(date.month)) == 1:
        month = "0"+str(date.month)


    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{month}-{day}_{location}.json"
 
    # Gets request and loads it
    r = requests.get(url)
    json_2 = r.text
    loaded = json.loads(json_2)

    data = {}
    kWh = []
    time_start = []
    
    # Iterates through a list of dictionaries and adds to list
    for i in loaded:
            kWh.append(float(list(i.values())[0]))
            date_string = list(i.values())[3]
            time_start.append(datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z"))

    # Add lists to dictionary data
    data["time_start"] = time_start
    data["NOK_per_kWh"] = kWh

    return(pd.DataFrame.from_dict(data))


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1" : "Oslo",
    "NO2" : "Kristiansand",
    "NO3" : "Trondheim",
    "NO4" : "Tromsø",
    "NO5" : "Bergen"
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations=tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    arguments:
        end_date (datetime.date) : a date object
        dats (int) : Integer of how many days timespan wanted
        locations (tuple) : a tuple of locations wanted
    return:
         dataframe : a dataframe with all prices from the given timespan
    """
    frames = []

    # Set day to today if not specified
    if end_date is None:
        end_date = datetime.date.today()

    # Iterate through locations and days and fetch the prices for each day
    for loc in locations:
        for i in range(days):
            date = end_date - timedelta(days = i)
            dataframe = fetch_day_prices(date, loc)
            dataframe["location_code"] = loc  
            dataframe["location"] = LOCATION_CODES[loc]
            frames.append(dataframe)
            
    # Concat the frames into a dataframe
    df = pd.concat(frames)

    return(df)


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    arguments:
        df (pd.DataFrame) : a dataframe with data of time and prices

    return:
        alt.Chart : a chart which we can see the data from the DataFrame
    """
    df['time_start'] = df['time_start'].astype(str)

    d = alt.Chart(df).mark_line().encode(
    x=alt.X("time_start:T", title="date"),
    y=alt.Y("NOK_per_kWh:Q", title="NOK / kWH"),
    color="location")

    return(d)


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    df['time_start'] = df['time_start'].astype(str)
    
    d = alt.Chart(df).mark_line().transform_window(
    avg="mean(NOK_perkWh)").encode(
    x="time_start:T",
    y="NOK_per_kWh:Q")

    return(d)


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()

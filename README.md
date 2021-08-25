# FotMob-PL-Webscraper

This is the code repository for scraping football (real football) data from [FotMob](https://fotmob.com). FotMob is a popular app for all-things football-- from live lineups and player ratings to key match statistics and injury news.

## About

Currently, the code is able to scrape match statistics by the Matchweek for the Premier League. It works from [this page](https://www.fotmob.com/leagues/47/matches/premier-league/by-round), going through each match and gathering statistics. It is powered by [Selenium](https://selenium-python.readthedocs.io/), a browser automation package. The final output is a csv containing match statistics such as xG (expected goals), xGOT, (expected goals on target), opposition half passes, possession, interceptions, duels, and much more for each team that played in the matchweek you specify.

## How To Use

First, simply download the python file and ensure selenium and pandas packages are installed on your computer. Second, you will need a chromedriver which you can download [here](https://sites.google.com/chromium.org/driver/). Once downloaded, just copy the file path of the chromedriver.exe file into the code (where you see the global variable DRIVER_PATH. Now you are all set to scrape! You can toggle which Matchweek you would like to scrape by changing the MATCHWEEK global variable.

## Example

To see an example output, download the csv file in the repo.

## Future Work

Currently, this is a scraper for only Premier League data. Further, it does not currently report shot map data (location, shot type, shot result). Future commits will include collecting and reporting these data, as well as functionality for other leagues (such as La Liga, Bundesliga, Serie A, etc.).

## Disclaimer

This project is strictly for educational and research purposes. This software is not intended to be used commercially whatsoever.


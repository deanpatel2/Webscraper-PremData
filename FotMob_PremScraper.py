# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 12:09:40 2021

@author: Dean Patel

FotMob Premier League Matchweek Stat Scraper
**FOR EDUCATIONAL PURPOSES ONLY**
"""
#%%
#Libraries
from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd

#%%
#Setting up driver and url
DRIVER_PATH = 'C:/Users/deanp/Downloads/chromedriver_win32/chromedriver.exe' # YOUR PATH GOES HERE
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.fotmob.com/leagues/47/matches/premier-league/by-round')

#%%
MATCHWEEK = 1 # HERE PUT THE MATCHWEEK YOU WANT TO SCRAPE STATS FOR
# identify dropdown with Select class
sel = Select(driver.find_element_by_class_name('css-ph6ea9-Select'))
sel.select_by_value (str(MATCHWEEK))
#%%
#Block to retrieve match links for the matchweek
match_divs = driver.find_elements_by_class_name('css-1ty7xja-LeagueMatchCSS')
match_links = []
for match in match_divs:
    link = match.find_element_by_tag_name('a').get_attribute('href')
    link = link.replace("matchfacts", "stats")
    match_links.append(link)

#%%
#Function to get match statistics given a match link and driver element
def get_match_stats(driver, match_link):
    driver.get(match_link) 
    div1 = driver.find_element_by_class_name('css-hhl4y6-MFStatsContainer')
    statsContainers = div1.find_elements_by_class_name('css-1khnrgx-StatsContainer')
    
    #Setup
    home_stats = []
    away_stats = []
    
    #Block to get team names and goals for, against
    header = driver.find_element_by_class_name('eb9uzl80')
    match_info = header.find_elements_by_tag_name('span')
    home_team = match_info[0].text
    away_team = match_info[3].text
    home_stats.append(home_team)
    away_stats.append(away_team)
    score = match_info[1].text
    home_goals = score[0]
    away_goals = score[4]
    home_gd = int(home_goals) - int(away_goals)
    away_gd = home_gd * -1
    home_stats.append(home_goals)
    home_stats.append(away_goals)
    home_stats.append(home_gd)
    away_stats.append(away_goals)
    away_stats.append(home_goals)
    away_stats.append(away_gd)
    
    #Block to get possession stats from a single match
    possession_graph = statsContainers[0].find_element_by_class_name('css-pqh9gi-MFSGraphContainer')
    possession_nums = possession_graph.find_elements_by_tag_name("div")
    possession_home = possession_nums[0].get_attribute('width')
    possession_away = possession_nums[1].get_attribute('width')
    home_stats.append(possession_home)
    away_stats.append(possession_away)

    #Block to loop through stat containers, extracting data for home and away
    for statContainer in statsContainers:
        statRowWrappers = statContainer.find_elements_by_class_name('e1car83v2')
        for statRowWrapper in statRowWrappers:
            statRow = statRowWrapper.find_elements_by_tag_name('span')
            home_stats.append(statRow[0].text)
            away_stats.append(statRow[2].text)
    return home_stats, away_stats

#%%
#Block to create DataFrame and export as a csv
matchweek_lists = []
labels = ['Team', 'GF', 'GA', 'GD', 'Posession', 'Expected goals (xG)', 'Total shots', 'Chances created', 'Big chances', 'Accurate passes', 'Pass success', 'Fouls conceded', 'Corners', 'Offsides', 'Shots', 'Shots on target', 'Shots off target', 'Blocked shots', 'Shots woodwork', 'Shots inside box', 'Shots outside box', 'Expected goals (xG)', 'xG first half', 'xG second half', 'xG on target (xGOT)', 'xG open play', 'xG set play', 'Accurate passes', 'Own half', 'Opposition half', 'Passes', 'Pass success', 'Touches', 'Long balls', 'Accurate long balls', 'Crosses', 'Accurate crosses', 'Throws', 'Duels won', 'Duels', 'Dribbles attempteds', 'Dribbles succeeded', 'Tackles attempted', 'Tackles succeeded', 'Aerials won', 'Interceptions', 'Discipline', 'Yellow cards', 'Red cards', 'Keeper', 'Saves', 'Diving saves', 'Saves inside box', 'Acted as sweeper', 'Punches']

for match_link in match_links:
    home_stats, away_stats = get_match_stats(driver, match_link)
    if len(home_stats) and len(away_stats) == 56: # deletes penalty xG data
        del home_stats[27]
        del away_stats[27]
    matchweek_lists.append(home_stats)
    matchweek_lists.append(away_stats)

matchweek_df = pd.DataFrame(matchweek_lists, columns=labels)
del matchweek_df['Discipline']
del matchweek_df['Keeper']

#%%

#Export as csv
matchweek_df.to_csv('PL_matchweek_' + str(MATCHWEEK) + '.csv', index=False)



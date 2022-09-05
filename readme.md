# ESPN Fantasy Baseball League Project

## Overview

I started this project to develop a solution for analyzing my fantasy baseball league data using external data sources instead of the standard statistics available on ESPN.

I wrote python code to collect, cleanse, shape, and merge the data accordingly. I also used Tableau to create custom interactive views of the data in order to make more relevant and meaningful in-season adjustments.

I hoped to gain an edge during the season by measuring player performance based on both current and historical advanced metric data, which ESPN does not provide on its fantasy website.

## Data Sources, Packages, and Tools

I connected to my private fantasy league on ESPN and accessed all of its data using this [espn-api](https://github.com/cwendt94/espn-api) python package.

I collected advanced metric data from [Baseball Savant](https://baseballsavant.mlb.com/) and [FanGraphs](https://www.fangraphs.com/) using this [pybaseball](https://github.com/jldbc/pybaseball) python package.

I connected all of the data coming from disparate sources using this [Player ID Map](https://www.smartfantasybaseball.com/tools/) tool, which provides the unique identifiers for players across each major sports website.

## Files

### *boxscores.py* 

Code to pull all matchup period results, including stat category totals, and W-L-T records for each team. It returns a final *boxscores.csv* dataset.

### *idmap.py* 

Code using *SFBB Player ID Map - PLAYERIDMAP.csv* to link players to their corresponding **ESPN, Statcast (MLB), and FanGraphs** unique identifiers.

### *stats_fangraphs.py* and *stats_statcast.py*

Code using packages to fetch the Statcast batter data and FanGraphs batter and pitcher data, and shapes the data frames accordingly.

### *colkeys_fangraphs_batter.txt* and *colkeys_fangraphs_pitcher.txt*

Contains the column index number and column name of all available metrics from FanGraphs. They are used as references when determining the desired data frame outputs.

### *stats.py*

Final code to fetch data from both sources, and for a specified range of seasons. It returns two final cleansed datasets: *stats_statcast.csv* and *stats_fangraphs.csv*.
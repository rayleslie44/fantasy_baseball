# imports
import pandas as pd
import numpy as np
from idmap import rosters_fangraphs
from pybaseball import batting_stats
from pybaseball import pitching_stats

# create function to get fangraphs data for batters and pitchers
def get_fangraphs_data(x, y):

    if y == 'Batter':

        # get batter data for specific year
        data = batting_stats(x).rename({'IDfg': 'IDFANGRAPHS'}, axis=1)

        # filter batters
        players = rosters_fangraphs[rosters_fangraphs['Batter/Pitcher']=='{}'.format(y)].reset_index(drop=True)

        # grab team id and fangraphs id columns
        players = players.iloc[:,[0,2]]

        # drop player ids that are not numeric
        players = players[pd.to_numeric(players['IDFANGRAPHS'], errors='coerce').notnull()].reset_index(drop=True)

        # convert player ids to int
        players['IDFANGRAPHS'] = players['IDFANGRAPHS'].astype(int)

        # merge fangraphs batter data with rosters
        stats = data.merge(players, on='IDFANGRAPHS', how='left').rename({'Team ID': 'team_id', 'IDFANGRAPHS': 'fg_id', 'Events': 'BBE', 'xBA': 'xAVG'}, axis=1)

        # fill team id nulls with 0 to denote player is free agent (not rostered)
        stats['team_id'] = stats['team_id'].fillna(0).astype(int)

        # use certain metric columns only
        stats_f = stats.iloc[:, np.r_[0:6, 7, 12:16, 22, 24, 35, 36, 38, 39, 41, 42, 51, 62, 103, 111, 112, 313, 314, 316:320]].reset_index(drop=True)
        
        # create new metric_diff columns
        stats_f['AVG_diff'] = (stats_f['AVG'] - stats_f['xAVG']).round(3)
        stats_f['SLG_diff'] = (stats_f['SLG'] - stats_f['xSLG']).round(3)
        stats_f['wOBA_diff'] = (stats_f['wOBA'] - stats_f['xwOBA']).round(3)

        # create new player type column - specifying batter
        stats_f['player_type'] = '{}'.format(y)

        # create long data frame
        df = pd.melt(stats_f, id_vars=['team_id', 'fg_id', 'Season', 'Name', 'Team', 'player_type', 'Age', 'G', 'PA', 'BBE'], var_name='metric', value_name='value')
    
    elif y == 'Pitcher':
        
        # get pitcher data for specific year
        data = pitching_stats(x).rename({'IDfg': 'IDFANGRAPHS'}, axis=1)

        # filter pitchers
        players = rosters_fangraphs[rosters_fangraphs['Batter/Pitcher']=='Pitcher'].reset_index(drop=True)

        # grab team id and fangraphs id columns
        players = players.iloc[:,[0,2]]

        # drop player ids that are not numeric
        players = players[pd.to_numeric(players['IDFANGRAPHS'], errors='coerce').notnull()].reset_index(drop=True)

        # convert player ids to int
        players['IDFANGRAPHS'] = players['IDFANGRAPHS'].astype(int)
        
        # merge fangraphs batter data with rosters
        stats = data.merge(players, on='IDFANGRAPHS', how='left').rename({'Team ID': 'team_id', 'IDFANGRAPHS': 'fg_id', 'TBF': 'PA', 'Events': 'BBE', 'HardHit': '95MPH+'}, axis=1)

        # fill team id nulls with 0 to denote player is free agent (not rostered)
        stats['team_id'] = stats['team_id'].fillna(0).astype(int)

        # use certain metric columns only
        stats_f = stats.iloc[:, np.r_[0:6, 8, 9, 13, 16, 26, 40, 43:46, 47, 63, 111, 114, 323:332, 333, 334]].reset_index(drop=True)
        
        # create new metric columns
        stats_f['Barrels/BBE%'] = (stats_f['Barrels']/stats_f['BBE']).round(3)
        stats_f['Barrels/PA%'] = (stats_f['Barrels']/stats_f['PA']).round(3)
        stats_f['ERA_diff'] = (stats_f['ERA'] - stats_f['xERA']).round(2)
        stats_f['FIP_diff'] = (stats_f['FIP'] - stats_f['xFIP']).round(2)
        
        # create new player type column - specifying pitcher
        stats_f['player_type'] = '{}'.format(y)

        # create long data frame
        df = pd.melt(stats_f, id_vars=['team_id', 'fg_id', 'Season', 'Name', 'Team', 'player_type', 'Age', 'G', 'PA', 'BBE'], var_name='metric', value_name='value')
    
    # return data frame
    return df
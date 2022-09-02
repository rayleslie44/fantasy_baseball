# imports
import pandas as pd
import numpy as np
from idmap import rosters_statcast
from pybaseball import statcast_batter_exitvelo_barrels

# create function to apply metric type
def f_metric_type(row):
    
    if row['metric'] in ('maxEV', 'avgEV', 'FB/LD', 'GB'):

        return 'Exit Velocity (MPH)'
    
    elif row['metric'] in ('maxDist', 'avgDist', 'avgHRDist'):

        return 'Distance (ft)'

    elif row['metric'] in ('95MPH+', 'HardHit%'):

        return 'Hard Hit'
    
    elif row['metric'] in ('#Barrels', 'Brls/BBE%', 'Brls/PA%'):

        return 'Barrels'
    
    elif row['metric'] in ('LA', 'SwSp%'):

        return 'Angle'

# create function to get statcast batter exit velocity and barrels data
def get_statcast_data(x):
    
    # get data for specific year
    batter_data = statcast_batter_exitvelo_barrels(x).rename({'player_id': 'MLBID'}, axis=1)
    
    # filter batters
    batters = rosters_statcast[rosters_statcast['Batter/Pitcher']=='Batter'].reset_index(drop=True)

    # grab team id and mlb id columns
    batters_s = batters.iloc[:,[0,2]].reset_index(drop=True)

    # convert mlb id to int
    batters_s['MLBID'] = batters_s['MLBID'].astype(int)

    # join statcast batter data with rosters
    batter_stats = batter_data.merge(batters_s, on='MLBID', how='left').rename({'Team ID': 'team_id', 'MLBID': 'mlb_id', ' first_name': 'first_name', 'attempts': 'BBE', 'avg_hit_angle': 'LA', 'anglesweetspotpercent': 'SwSp%', 'max_hit_speed': 'maxEV', 'avg_hit_speed': 'avgEV', 'fbld': 'FB/LD', 'gb': 'GB', 'max_distance': 'maxDist', 'avg_distance': 'avgDist', 'avg_hr_distance': 'avgHRDist', 'ev95plus': '95MPH+', 'ev95percent': 'HardHit%', 'barrels': '#Barrels', 'brl_percent': 'Brls/BBE%', 'brl_pa': 'Brls/PA%'}, axis=1)
    
    # fill team id nulls with 0 to denote player is free agent (not rostered)
    batter_stats['team_id'] = batter_stats['team_id'].fillna(0).astype(int)

    # create long data frame
    batter_df = pd.melt(batter_stats, id_vars=['team_id', 'last_name', 'first_name', 'mlb_id', 'BBE'], var_name='metric', value_name='value')

    # apply function to create metric type column
    batter_df['metric_type'] = batter_df.apply(lambda row: f_metric_type(row), axis=1)

    # create season column
    batter_df['season'] = x

    # reorder columns
    batter_df = batter_df[['team_id', 'season', 'mlb_id', 'last_name', 'first_name', 'BBE', 'metric_type', 'metric', 'value']]

    # return data frame
    return batter_df
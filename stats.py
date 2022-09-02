# imports
import pandas as pd
from stats_fangraphs import get_fangraphs_data
from stats_statcast import get_statcast_data

# create list of years to pull data for
years = [2022, 2021, 2020]

# create list of both player types to pull fangraphs data for
types = ['Batter', 'Pitcher']

# create list of data frames to store appended results
stats_statcast = pd.DataFrame()
stats_fangraphs = pd.DataFrame()

# grab stats for each year and each player type
for year in years:
    
    # statcast batter data
    df_s = get_statcast_data(year)

    stats_statcast = stats_statcast.append(df_s)

    # fangraphs batter and pitcher data
    for type in types:

        df_f = get_fangraphs_data(year, type)

        stats_fangraphs = stats_fangraphs.append(df_f)

# define data frames to save
names = ['stats_statcast', 'stats_fangraphs']
frames = [stats_statcast, stats_fangraphs]

# save data frames to csv
for name, data in zip(names, frames):

    data.to_csv('{}.csv'.format(name), index=False)
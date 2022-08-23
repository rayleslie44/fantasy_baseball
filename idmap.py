# import libraries
import pandas as pd

# import rosters from ESPN API
from config import rosters

# create function that labels positions by batter or pitcher
def label_position(row):
    
    if row['Position'] == 'P':
        
        return 'Pitcher'
    
    elif row['Position'] == 'OF' or 'C' or 'DH' or '1B' or '2B' or '3B' or 'SS':
        
        return 'Batter'
    
    else:
        
        return 'NA'

# create function to map player ids
def map_ids(x):
    
    # get mlb ids for statcast
    if x == 'statcast':

        id = 'MLBID'
        name = 'MLBNAME'
    
    # get ids for fangraphs
    elif x == 'fangraphs':

        id = 'IDFANGRAPHS'
        name = 'FANGRAPHSNAME'
    
    # use palyer id mapping tool here: https://www.smartfantasybaseball.com/PLAYERIDMAPCSV
    idmap = pd.read_csv('SFBB Player ID Map - PLAYERIDMAP.csv', usecols=['ESPNID', '{}'.format(id), '{}'.format(name), 'POS']).rename({'POS': 'Position'}, axis=1)
    
    # merge rosters by ESPN id to get ids
    merge1 = rosters.merge(idmap, how='left', on='ESPNID')
    
    # create data frame of players that were not found
    nulls = merge1[merge1.isnull().any(axis=1)].reset_index(drop=True)

    # drop unused columns
    nulls.drop(['{}'.format(name), 'Position', '{}'.format(id), 'ESPNID'], axis=1, inplace=True)

    # rename column to match column in player id map
    nulls.rename({'Player': '{}'.format(name)}, axis=1, inplace=True)

    # merge nulls by player name to get id
    merge2 = nulls.merge(idmap, how='left', on='{}'.format(name))

    # rename back to player
    merge2.rename({'{}'.format(name): 'Player'}, axis=1, inplace=True)

    # drop unused column
    merge1.drop('{}'.format(name), axis=1, inplace=True)

    # drop duplicate players
    merge1 = merge1.dropna()

    # create dataframe of all players found by id and name
    df_ids = merge1.append(merge2).reset_index(drop=True)

    # drop players not found in player id map
    df_ids = df_ids.dropna(subset=['{}'.format(id)]).reset_index(drop=True)

    # apply function on new column to label players as batter or pitcher
    df_ids['Batter/Pitcher'] = df_ids.apply(lambda row: label_position(row), axis=1)

    # reorder columns
    df_ids = df_ids[['Team ID', 'ESPNID', '{}'.format(id), 'Player', 'Team', 'Injury Status', 'Position', 'Batter/Pitcher']]

    # OPTIONAL CODE TO TEST FOR PLAYER NON MATCHES BETWEEN DATA FRAMES
    # create lists for two player data frames
    #list1 = df_ids['Player']
    #list2 = rosters['Player']
    
    # create set to find difference between lists
    #non_matches = list(set(list1).difference(list2))
    
    # option to return as series
    # new_series = pd.Series(new_list)
    
    # print counts of players in each data frame
    #print('{}'.format(x))
    #print('rosters:',rosters.shape[0])
    #print('merge1:', merge1.shape[0])
    #print('merge2:', merge2.shape[0])
    #print('rosters_df:', df_ids.shape[0])
    #print('non_matches:', len(non_matches))

    return df_ids

# create statcast rosters data frame
rosters_statcast = map_ids('statcast')

# create fangraphs rosters data frame
rosters_fangraphs = map_ids('fangraphs')
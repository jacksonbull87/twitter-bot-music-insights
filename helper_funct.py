import datetime
import pandas as pd
from cm_api import get_fan_metrics, get_api_token
from cm_config import config
import time

rt = config['refresh_token']
api_token = get_api_token(rt)

def generate_date_one_year_ago():
    date = datetime.datetime.now() - datetime.timedelta(days=365)
    return str(date.date())

def generate_today_date():
    date = datetime.datetime.now()- datetime.timedelta(days=0)
    return str(date.date())

def generate_yesterday_date():
    date = datetime.datetime.now()- datetime.timedelta(days=1)
    return str(date.date())

def generate_one_week_prior_date():
    date = datetime.datetime.now()- datetime.timedelta(days=7)
    return str(date.date())


def parse_data(data):
    return data[0]['name'].title(), data[0]['artist_names'][0]

def parse_viral(data):
    data_bucket = []
    for track in data:
        track_tuple = (track['name'], track['tiktok_artist_names'][0], track['isrc'], track['velocity'], track['cm_track'])
        data_bucket.append(track_tuple)

    df = pd.DataFrame(data_bucket, columns=['title', 'artist', 'isrc', 'velocity', 'cm_id'])
    df.dropna(subset=['isrc'], inplace=True)
    df.sort_values('velocity', ascending=False, inplace=True)
    df1 = df.reset_index()
    return df1['title'][0], df1['artist'][0], df1['velocity'][0], df1['cm_id'][0]

def parse_top200_popularity(data):
    data_bucket = []
    for track in data:
        track_tuple = (track['name'], track['spotify_artist_names'], track['cm_artist'], track['spotify_popularity'])
        data_bucket.append(track_tuple)

    df = pd.DataFrame(data_bucket, columns=['title', 'artists', 'artist ids', 'current spotify popularity'])
    return df


def add_popularity_before_after(api_token, before_date, current_date, dataframe):
    #return dataframe with before, after, and change in popularity for primary artist
    counter = 0
    before_popularity = []
    for artist_id in dataframe['artist ids']:
        popularity_data = get_fan_metrics(api_token, artist_id[0], 'spotify', before_date,before_date, field='popularity')
        if popularity_data['popularity']:
            before_popularity.append(popularity_data['popularity'][0]['value'])
        else:
            before_popularity.append('NaN')
        counter+=1
        print(counter)

        time.sleep(4)

    dataframe['before popularity'] = pd.Series(before_popularity) 
    
    
    current_artist_popularity_list = []
    for artist_id in dataframe['artist ids']:
        current_popularity_data = get_fan_metrics(api_token, artist_id[0], 'spotify', current_date, current_date, field='popularity')
        if current_popularity_data['popularity']:
            current_artist_popularity_list.append(current_popularity_data['popularity'][0]['value'])
        else:
            current_artist_popularity_list.append('NaN')
        counter+=1
        print(counter)
        time.sleep(4)

    dataframe['current_artist_popularity'] = pd.Series(current_artist_popularity_list)
    
    df1 = dataframe[~dataframe['current_artist_popularity'].isin(['NaN'])]
    df2 = df1[~df1['before popularity'].isin(['NaN'])]
    df2['popularity change'] = df2['current_artist_popularity'] - df2['before popularity']
    return df2

def get_most_successful_artist(dataframe):
    #returns title, artist, before popularity, current popularity, popularity change
    df3 = dataframe.sort_values('popularity change', ascending=False).reset_index()
    return df3['title'][0], df3['artists'][0][0], df3['artist ids'][0][0], df3['before popularity'][0],  df3['current_artist_popularity'][0], df3['popularity change'][0]
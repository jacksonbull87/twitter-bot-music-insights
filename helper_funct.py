import datetime
import pandas as pd
from cm_api import get_fan_metrics, get_api_token
from cm_config import config
import time
import requests

rt = config['refresh_token']
api_token = get_api_token(rt)

def get_date_range(start_date, end_date, frequency):
    
    return [str(x)[:10] for x in list(pd.date_range(start=start_date,end=end_date, freq=frequency))]

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

def generate_one_month_ago():
    date = datetime.datetime.now()- datetime.timedelta(days=30)
    return str(date.date())


def parse_data(data):
    return data[0]['name'].title(), data[0]['artist_names'][0]

def parse_tiktok_data(data):
    data_bucket = []
    for track in data:
        track_tuple = (track['name'], track['tiktok_artist_names'][0], track['isrc'], track['velocity'], track['cm_track'])
        data_bucket.append(track_tuple)

    df = pd.DataFrame(data_bucket, columns=['title', 'artist', 'isrc', 'velocity', 'cm_id'])
    df.dropna(subset=['isrc'], inplace=True)
    return df

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

def get_most_social_gain(dataframe):
    #returns title, artist, before popularity, current popularity, popularity change
    df3 = dataframe.sort_values('follower_diff', ascending=False).reset_index()
    return df3['title'][0], df3['artists'][0][0], df3['artist ids'][0][0], df3['before'][0] ,df3['follower_diff'][0]

def get_most_listener_gain(dataframe):
    #returns title, artist, before popularity, current popularity, popularity change
    df3 = dataframe.sort_values('listener_diff', ascending=False).reset_index()
    return df3['title'][0], df3['artist'][0], df3['cm_artist_id'][0], df3['before'][0] ,df3['listener_diff'][0]

#this functions takes in a dataframe and a platform for which to collect data on the difference in followers between two dates
#platform values are   `instagram`, `twitter`
def get_follower_differnce(api_token, dataframe, platform, start_date, end_date):
    ig_bucket = []
    for artist in dataframe['artist ids']:
        followers = get_fan_metrics(api_token, artist[0], platform, start_date, end_date, field='followers')['followers']
        if len(followers) > 0:
            follow_tuple = (followers[0]['value'], followers[-1]['value'])
            ig_bucket.append(follow_tuple)
        else:
            follow_tuple = (None, None)
            ig_bucket.append(follow_tuple)

    df = pd.DataFrame(ig_bucket, columns=['before', 'after'])

    joined_data = dataframe.join(df)
    joined_data['follower_diff']  = joined_data['after'] - joined_data['before']
    return joined_data


def count_wiki_views(list_of_dict):
    counter = 0
    for item in list_of_dict:
        counter += item['value']
    return counter

def get_topwiki_artist(dataframe):
    return dataframe['title'][0], dataframe['artist'][0],dataframe['cm_artist_id'][0], dataframe['wiki views'][0]


#retreive title, artist, velocity
def most_viral_tiktoktrack(dataframe):
    return dataframe['add date'][0], dataframe['title'][0], dataframe['artist'][0], dataframe['velocity'][0], dataframe['cm_artist_id'][0]

#get top spotify monthly cities
def monthly_listen(api_token, cm_artist_id, since_date):
    response = requests.get(url='https://api.chartmetric.com/api/artist/{}/where-people-listen'.format(cm_artist_id),
                           headers={'Authorization' : 'Bearer {}'.format(api_token)},
                           params={'since':since_date})
    
    if response.status_code == 200:
        return response.json()['obj']
    else:
        print(response.status_code)
        print(response.text)


def top_5_cities(data_object):
    city_list = list(data_object.keys())
    return city_list[0],city_list[1],city_list[2],city_list[3], city_list[4]


import pandas as pd
from cm_api import *

#function to parse data list into pandas dataframe
def create_dataframe(data_list):
    top_tracks_bucket = []
    for track in data_list:
        track_tuple = (track['id'], track['name'], track['isrc'], track['cm_track'],
                      track['artist'], track['artist_names'], track['album_title'], 
                       track['album_names'], track['rank'], track['added_at'], track['created_at'],
                       track['country'],
                      track['genre'], track['kind'], track['playcount_all'], 
                       track['playcount_weekly'], 
                       track['velocity'], track['time_on_chart'])
        top_tracks_bucket.append(track_tuple)

    top_df = pd.DataFrame(top_tracks_bucket, columns=['SC ID', 'title', 'isrc', 'cm_track_id', 'artist', 'artist_names', 'album_title', 'album_names', 'rank',
                                            'added_at','created_at', 'country', 'genre', 'kind', 'total_playcount', 'weekly_playcount', 'velocity', 'time_on_chart'])
    return top_df

#create a list of unique values given an array
def unique(series):
    return list(series.unique())

#create a dictionary from a list of tuples
def Convert(tup, di):
    new_tup = [x for x in tup if x != None and type(x) == tuple]
    di = dict(new_tup)
    return di 

#Given specified parameters, this function returns a dictionary of each artist's fan metric
def artist_fanmetric_dict(artist_id_dict, api_token, source, since_date, until_date, field_value, dict_value):
    #dictionary_values: weekly_diff, weekly_diff_percent, monthly_diff, monthly_diff_percent, value
    bucket = []
    for k,v in artist_id_dict.items():
        listener_data = get_fan_metrics(api_token, v, source, since_date,until_date,field=field_value)[field_value]
        if len(listener_data) > 0:
            monthly_li_tu = (k.lower(), listener_data[0][dict_value])
            bucket.append(monthly_li_tu)
        else:
            continue
    dictionary = {}    
    di = Convert(bucket, dictionary)
    return di
    

#new feature of percent change is artist listeners
def percent_change(x):
    return ((x[1]- x[0])/x[0])*100

#remove trailing zeros from cm artist ids
def remove_trailing_zeros(number):
    from decimal import Decimal
    return str(number).rstrip('0').rstrip('.')

#finds tracks max velocity in dataframe
def get_tracks_maxv(title, dataframe):
    #input track title, return title's max velocity
    return dataframe.loc[dataframe['title'] == title]['velocity'].max()

def get_tracks_peak_weeklycount(title, dataframe):
    #input track title, return title's max velocity
    return dataframe.loc[dataframe['title'] == title]['current_plays'].max()


def get_tracks_peak_rank(title, dataframe):
    #input track title, return title's max velocity
    return dataframe.loc[dataframe['title'] == title]['rank'].min()

#this function takes in a string argument and returns the first tag
#of the resulting list
def isolate_first_tag(tag_string):
    if tag_string:
        return tag_string.split(',')[0]
    else:
        return 'N/A'

def insert_thousands_commas(number):
    return '{:0,.0f}'.format(number)

def get_summary_statistics(dataset):
    import numpy as np
    mean = int(np.round(np.mean(dataset), 0))
    median = int(np.round(np.median(dataset), 2))
    min_value = int(np.round(dataset.min(), 2))
    max_value = int(np.round(dataset.max(), 2))
    quartile_1 = int(np.round(dataset.quantile(0.25), 2))
    quartile_3 = int(np.round(dataset.quantile(0.75), 2))
    # Interquartile range
    iqr = np.round(quartile_3 - quartile_1, 2)
    print('Min: %s' % insert_thousands_commas(min_value))
    print('Mean: %s' % insert_thousands_commas(mean))
    print('Max: %s' % insert_thousands_commas(max_value))
    print('25th percentile: %s' % insert_thousands_commas(quartile_1))
    print('Median: %s' % insert_thousands_commas(median))
    print('75th percentile: %s' % insert_thousands_commas(quartile_3))
    print('Interquartile range (IQR): %s' % insert_thousands_commas(iqr))
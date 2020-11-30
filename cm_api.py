#This module contains api functions to retrieve raw data from Chartmetric's servers
import requests
import re
import pandas as pd
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



def get_api_token(REFRESH_TOKEN):
    api_url = 'https://api.chartmetric.com/api/token'
    
    response = requests.post(url=api_url, data={'refreshtoken' : REFRESH_TOKEN}, 
                             json={'Content-Type' : 'application/json'})
    results = response.json()
    api_token = results['token']
    return api_token

##################################################################################
def search(api_token, track_name, artist_name, search_type='tracks', limit=10):
    #returns dataframe of all tracks that satisfy user search criteria
    response = requests.get(url='https://api.chartmetric.com/api/search',
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, 
                            params={'q':track_name, 'type':search_type, 'limit':limit})
    if response.status_code == 200:

        data = response.json()
        track = data['obj']
        
        data_bucket = []
        for item in track['tracks']:

            if re.match(track_name.lower(), item['name'].lower()) and re.match(artist_name.lower(), item['artist_names'][0].lower()):
                track_tuple = (item['isrc'], item['name'], item['cm_track'], item['artist_names'][0],item['cm_artist'], item['album_names'][0], 
                              item['release_dates'][0])
                data_bucket.append(track_tuple)

                print("isrc #: ", item['isrc'])
                print("track name : ", item['name'])
                print("chartmetric ID : ", item['cm_track'])
                print("artist name : ", item['artist_names'][0])
                print("album name : ", item['album_names'][0])
                print("release date : ", item['release_dates'][0])
                print("Chartmetric Artist ID: , item['cm_artist'][0]")
                print('\n')

        return pd.DataFrame(data_bucket, columns=['isrc', 'track', 'chartmetric id', 'artist','cm artist id' 'album', 'release date'])
    else:
        pass

def get_track_metadata(api_token, cm_track_id):
    #cm_track_id refers to the chartmetric track id associated with the song
    #returns a dictionary('id', 'name', 'isrc', 'image_url', 'duration_ms', 'composer_name', 
    #'artists', 'albums', 'tags', 'cm_audio_features', 'release_date', 'lastfm', 'cm_statistics')
    response = requests.get(url='https://api.chartmetric.com/api/track/{}'.format(cm_track_id),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}
                                )
    if response.status_code == 200:

        data = response.json()
        track = data['obj']
    else:
        pass
    return track

def get_chart_data(api_token, cm_track_id, chart_type, date):
    #refer to https://api.chartmetric.com/apidoc/#api-Track-getTrackCharts for allowed values for chart_type
    #date == YYYY-MM-DD
    #returns a list of dictionaries with chart data for each date
    response = requests.get(url='https://api.chartmetric.com/api/track/{}/{}/charts'.format(cm_track_id, chart_type),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, params={'since': date}
                                )
    if response.status_code == 200:
        data = response.json()
        chart = data['obj']
        return chart['data']

def get_tiktok_chart_data(api_token, chart_type, date, interval, limit=100):
    #for apitoken import get_import_token
    #for chart_type, accepted values include 'tracks', 'videos', 'users'
    #date == YYYY-MM-DD
    #for interval, accepted values include 'daily', 'weekly'
    #returns a list of song metadata
    response = requests.get(url='https://api.chartmetric.com/api/charts/tiktok/{}'.format(chart_type),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, params={'date': date, 'interval': interval, 'limit': limit}
                                )
    if response.status_code == 200:
        data = response.json()
        chart = data['obj']
        return chart['data']


def get_track_chart(api_token, cm_id, chart_type, since):
    response = requests.get(url='https://api.chartmetric.com/api/track/{}/{}/charts'.format(cm_id, chart_type),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, params={'since':since}
                                )
    if response.status_code == 200:
        data = response.json()
        chart = data['obj']
        return chart['data']
    else:
        print("Artist ID: ", cm_id)
        print(response.status_code)
        print(response.text)

def get_spotify_charts(api_token, date, country_code, chart_type, interval):
    response = requests.get(url='https://api.chartmetric.com/api/charts/spotify',
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, 
        params={'date':date, 'country_code':country_code, 'type':chart_type, 'interval':interval}
                                )
    if response.status_code == 200:
        data = response.json()
        chart = data['obj']
        return chart['data']
    else:
        
        print(response.status_code)
        print(response.text)

def get_spotify_url(api_token, cm_artist_id):
    
    response = requests.get(url='https://api.chartmetric.com/api/artist/{}/urls'.format(cm_artist_id),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)})
    if response.status_code == 200:

        data = response.json()['obj']
        for social in data:
            if social['domain'] == 'spotify':
                return social['url'][0]
    else:
        
        print(response.status_code)
        print(response.text)

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
    

def get_instagram_url(api_token, cm_artist_id):
    
    response = requests.get(url='https://api.chartmetric.com/api/artist/{}/urls'.format(cm_artist_id),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)})
    if response.status_code == 200:

        data = response.json()['obj']
        for social in data:
            if social['domain'] == 'instagram':
                return social['url'][0]
    else:
        
        print(response.status_code)
        print(response.text)


def get_track_playlist(api_token, cm_id, platform, status, since, limit):
    response = requests.get(url='https://api.chartmetric.com/api/track/{}/{}/{}/playlists'.format(cm_id, platform, status),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, params={'since':since, 'limit': limit}
                                )
    if response.status_code == 200:
        data = response.json()
        chart = data['obj']
        return chart
    else:
        print("Artist ID: ", cm_id)
        print(response.status_code)
        print(response.text)


def get_artist_id(api_token, q, search_type):
    #return tuple (artist name, artist cm id)
    response = requests.get(url='https://api.chartmetric.com/api/search',
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, params={'q': q, 'type': search_type,
                            'limit':50}
                                )
    if response.status_code == 200:
        data = response.json()
        try:
            chart = data['obj']
            for artist in chart['artists']:
                if re.fullmatch(q.lower(), artist['name'].lower()):
                    # print(artist['name'])
                    # print('Chartmetric ID: ',artist['id'])
                    return artist['id']
                else:
                    continue
            
        except TypeError:
            return "None"
    else:
        print(response.status_code)
        print(response.text)

def get_fan_metrics(api_token, cm_artist_id, source, since_date, until_date, field=None):
    #returns a list of dictionaries, each item being a different timestamp
    retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[ 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"], 
)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    response = http.get(url='https://api.chartmetric.com/api/artist/{}/stat/{}'.format(cm_artist_id, source),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, params={'since': since_date, 'field': field, 
                            'interpolated':True,'until':until_date}
                                )
    if response.status_code == 200:
        data = response.json()

        chart = data['obj']
        return chart
            
            
    else:
        print("Artist ID: ", cm_artist_id)
        print(response.status_code)
        print(response.text)

def get_instagram_audience(api_token, cm_artist_id):
    #returns a list of dictionaries, each item being a different timestamp
    response = requests.get(url='https://api.chartmetric.com/api/artist/{}/instagram-audience-stats'.format(cm_artist_id),
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}
                                )
    if response.status_code == 200:
        data = response.json()
        try:
            chart = data['obj']
            return chart
            
        except TypeError:
            return "None"
    else:
        print(cm_artist_id)
        print(response.status_code)
        print(response.text)


def get_shazam_most_viral_track(api_token,date, country_code='US'):
    response = requests.get(url='https://api.chartmetric.com/api/charts/shazam',
                            headers={'Authorization' : 'Bearer {}'.format(api_token)}, 
                            params={'country_code':country_code, 'date':date}
                                )
    if response.status_code == 200:
        data = response.json()
        tracks = data['obj']['data']
        data_bucket = []
        for track in tracks:
            if type(track['artist_names']) == type(list):

                track_tuple = (track['name'], track['artist_names'][0],track['velocity'], track['cm_artist'][0], track['isrc'])
                data_bucket.append(track_tuple)
            else:
                track_tuple = (track['name'], track['artist_names'],track['velocity'], track['cm_artist'], track['isrc'])
                data_bucket.append(track_tuple)        

        df = pd.DataFrame(data_bucket, columns=['title', 'artist','velocity', 'artist id', 'isrc'])
        df.dropna(subset=['isrc'], inplace=True)
        df.sort_values('velocity', ascending=False, inplace=True)
        df1 = df.reset_index()
        return df1['title'][0], df1['artist'][0][0], df1['velocity'][0], df1['artist id'][0][0]


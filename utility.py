from datetime import datetime
import requests

def api_reset_time(api_token):
    #converts unix timestamp to human time
    response = requests.get(url='https://api.chartmetric.com/api/charts/spotify',
                                headers={'Authorization' : 'Bearer {}'.format(api_token)}, 
            params={'date':'2020-10-22', 'country_code':'US', 'type':'regional', 'interval':'daily'})
    unix_timestamp = int(response.headers['X-RateLimit-Reset'])
    return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
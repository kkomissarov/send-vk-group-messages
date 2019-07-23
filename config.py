import os
API_KEY = os.environ['SAMOCVETY_API_KEY']
GROUP_ID = '179340014'
API_VERSION = '5.101'


base_request_params = {
    'access_token': API_KEY,
    'v': API_VERSION
}


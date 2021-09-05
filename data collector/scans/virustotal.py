from __future__ import print_function
import json
import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi
import requests
import json

API_KEY = 'API_KEY'
def vt_api(domain):
    url="http://"+domain

    params = {'apikey':API_KEY,'resource':url}

    url = 'https://www.virustotal.com/vtapi/v2/url/report'

    try:
        response = requests.get(url, params=params)
        json_=response.json()
        if json_['verbose_msg'] =="Resource does not exist in the dataset":
            result = 0
        else:
            result = json_['positives']
    except:
        result = 0
    return result

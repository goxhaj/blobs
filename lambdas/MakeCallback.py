import json
import requests
from urllib.parse import urlparse

from requests import exceptions

def execute(event, context):
    print (json.dumps(event))
    for record in event['Records']:
        if(record['eventName'] == 'MODIFY'):
            try:
                if(record['dynamodb']['NewImage']['callback_url'] is not None):
                    url = record['dynamodb']['NewImage']['callback_url']['S']
                    payload = record['dynamodb']['NewImage']['labels']['S']
                    if(url_validator(url)):
                        requests.post(url, data = payload)
                    else:
                        print ("Invalid URL: " + url + " callback method defined!")
            except Exception as e:
                print (str(e))


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

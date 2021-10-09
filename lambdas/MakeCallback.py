import json
from urllib.parse import urlparse

import backoff
import requests


def execute(event, context):
    print(json.dumps(event))
    for record in event['Records']:
        if record['eventName'] == 'MODIFY':
            try:
                if record['dynamodb']['NewImage']['callback_url'] is not None:
                    url = record['dynamodb']['NewImage']['callback_url']['S']
                    payload = record['dynamodb']['NewImage']['labels']['S']
                    if url_validator(url):
                        send_request(url, payload)
                    else:
                        print("Invalid URL: " + url + " callback method defined!")
            except Exception as e:
                print(str(e))


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_tries=10,
                      jitter=None)
def send_request(url, payload):
    requests.post(url, data=payload)


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

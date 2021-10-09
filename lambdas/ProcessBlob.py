import datetime
import json
import os
import random
import time
from urllib.parse import unquote_plus

import boto3
import botocore.exceptions

REGION = os.environ['REGION']
TABLE = os.environ['BLOBS_TABLE']
BUCKET_NAME = os.environ['BUCKET_NAME']
MAX_LABELS = os.environ['MAX_LABELS']

s3 = boto3.client('s3', region_name=REGION)
table = boto3.resource('dynamodb', region_name=REGION).Table(TABLE)
rekognition = boto3.client('rekognition')


def execute(event, context):
    print(">> EVENT")
    print(json.dumps(event))
    print("<< EVENT")

    for record in event['Records']:
        try:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            print(
                ">> PROCESS BLOB | REGION: " + REGION + " TABLE: " + TABLE + " BUCKET_NAME: " + bucket + " BUCKET_KEY: " + key)
            rekognition_response = rekognition.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': key}},
                                                             MaxLabels=int(MAX_LABELS))
            response = table.update_item(
                Key={
                    "blob_id": str(key)
                },
                UpdateExpression="set labels=:labels, dt_updated=:dt_updated",
                ExpressionAttributeValues={
                    ':labels': str(rekognition_response),
                    ':dt_updated': str(datetime.datetime.now())
                },
                ReturnValues="UPDATED_NEW"
            )
            print(response)

        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'ProvisionedThroughputExceededException':
                print("implement a backoff retry mechanism")
            if error.response['Error']['Code'] == 'InternalServerError':
                print("implement a backoff retry mechanism")
            if error.response['Error']['Code'] == 'ThrottlingException':
                print("implement a backoff retry mechanism")
            else:# there is no other way to process this image
                print(str(error))
                table.update_item(
                    Key={
                        "blob_id": str(key)
                    },
                    UpdateExpression="set error_message=:message, dt_updated=:dt_updated",
                    ExpressionAttributeValues={
                        ':message': str(error),
                        ':dt_updated': str(datetime.datetime.now())
                    },
                    ReturnValues="UPDATED_NEW"
                )
        except Exception as e:
            print(str(e))



def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def rwb(f):
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except:
                    if x == retries:
                        raise
                    else:
                        sleep = (backoff_in_seconds * 2 ** x +
                                 random.uniform(0, 1))
                        time.sleep(sleep)
                        x += 1

        return wrapper

    return rwb

import json
import requests
import unittest
import time

SERVICE = 'https://bj4wilra8f.execute-api.us-east-1.amazonaws.com/dev/blobs'
CALLBACK_URL = 'https://webhook.site/67679c5d-0e2a-47e6-8e73-1b53138bd617'
SLEEP = 1.5
CHECK_FOR_LABELS = False


class TestCases(unittest.TestCase):

    def test1(self):
        response_post = requests.post(SERVICE, json={'callback_url': str(CALLBACK_URL)})
        response_content = response_post.json()
        assert (response_post.status_code == 201)

        with open('images/test1.jpeg', 'rb') as image_file:
            response_put_s3 = requests.put(response_content["presigned_url"], data=image_file)
            assert (response_put_s3.status_code == 200)
            response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
            assert (response_get.status_code == 200)
            assert (response_get.json()["blob_id"] == response_content["blob_id"])
            assert (response_get.json()["callback_url"] == str(CALLBACK_URL))

            if CHECK_FOR_LABELS:
                time.sleep(SLEEP)
                response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
                labels_str = response_get.json()['labels']
                json_object = json.loads(labels_str.replace('\'', '\"'))

                for label in json_object['Labels']:
                    if label['Name'] == "Car":
                        assert (label['Confidence'] == 99.98123168945312)
                    if label['Name'] == "Vehicle":
                        assert (label['Confidence'] == 99.98123168945312)
                    if label['Name'] == "Transportation":
                        assert (label['Confidence'] == 99.98123168945312)

    def test2(self):
        response_post = requests.post(SERVICE, json={'callback_url': str(CALLBACK_URL)})
        response_content = response_post.json()
        assert (response_post.status_code == 201)

        with open('images/test2.png', 'rb') as image_file:
            response_put_s3 = requests.put(response_content["presigned_url"], data=image_file)
            assert (response_put_s3.status_code == 200)
            response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
            assert (response_get.status_code == 200)
            assert (response_get.json()["blob_id"] == response_content["blob_id"])
            assert (response_get.json()["callback_url"] == str(CALLBACK_URL))
            if CHECK_FOR_LABELS:
                time.sleep(SLEEP)
                response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
                labels_str = response_get.json()['labels']
                json_object = json.loads(labels_str.replace('\'', '\"'))

                for label in json_object['Labels']:
                    if label['Name'] == "Person":
                        assert (label['Confidence'] == 99.26136779785156)
                    if label['Name'] == "People":
                        assert (label['Confidence'] == 99.26136779785156)
                    if label['Name'] == "Family":
                        assert (label['Confidence'] == 97.70223236083984)

    def test3(self):
        response_post = requests.post(SERVICE, json={'callback_url': str(CALLBACK_URL)})
        response_content = response_post.json()
        assert (response_post.status_code == 201)

        with open('images/test3.jpeg', 'rb') as image_file:
            response_put_s3 = requests.put(response_content["presigned_url"], data=image_file)
            assert (response_put_s3.status_code == 200)
            response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
            assert (response_get.status_code == 200)
            assert (response_get.json()["blob_id"] == response_content["blob_id"])
            assert (response_get.json()["callback_url"] == str(CALLBACK_URL))
            if CHECK_FOR_LABELS:
                time.sleep(SLEEP)
                response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
                labels_str = response_get.json()['labels']
                json_object = json.loads(labels_str.replace('\'', '\"'))

                for label in json_object['Labels']:
                    if label['Name'] == "Bridge":
                        assert (label['Confidence'] == 99.01644134521484)
                    if label['Name'] == "Building":
                        assert (label['Confidence'] == 99.01644134521484)
                    if label['Name'] == "Suspension Bridge":
                        assert (label['Confidence'] == 95.12909698486328)

    def test4(self):
        response_post = requests.post(SERVICE, json={'callback_url': str(CALLBACK_URL)})
        response_content = response_post.json()
        assert (response_post.status_code == 201)

        with open('images/test4.JPG', 'rb') as image_file:
            response_put_s3 = requests.put(response_content["presigned_url"], data=image_file)
            assert (response_put_s3.status_code == 200)
            response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
            assert (response_get.status_code == 200)
            assert (response_get.json()["blob_id"] == response_content["blob_id"])
            assert (response_get.json()["callback_url"] == str(CALLBACK_URL))
            if CHECK_FOR_LABELS:
                time.sleep(SLEEP)
                response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
                labels_str = response_get.json()['labels']
                json_object = json.loads(labels_str.replace('\'', '\"'))
                for label in json_object['Labels']:
                    if label['Name'] == "Person":
                        assert (label['Confidence'] == 99.10224914550781)
                    if label['Name'] == "Grass":
                        assert (label['Confidence'] == 96.87136840820312)
                    if label['Name'] == "Plant":
                        assert (label['Confidence'] == 96.87136840820312)

    def test5(self):
        response_post = requests.post(SERVICE, json={'callback_url': str(CALLBACK_URL)})
        response_content = response_post.json()
        assert (response_post.status_code == 201)

        with open('images/test5.jpg', 'rb') as image_file:
            response_put_s3 = requests.put(response_content["presigned_url"], data=image_file)
            assert (response_put_s3.status_code == 200)
            response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
            assert (response_get.status_code == 200)
            assert (response_get.json()["blob_id"] == response_content["blob_id"])
            assert (response_get.json()["callback_url"] == str(CALLBACK_URL))
            if CHECK_FOR_LABELS:
                time.sleep(SLEEP)
                response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
                labels_str = response_get.json()['labels']
                json_object = json.loads(labels_str.replace('\'', '\"'))
                for label in json_object['Labels']:
                    if label['Name'] == "Plant":
                        assert (label['Confidence'] == 95.94786071777344)
                    if label['Name'] == "Food":
                        assert (label['Confidence'] == 92.54127502441406)
                    if label['Name'] == "Fruit":
                        assert (label['Confidence'] == 83.06842803955078)

    def test6(self):
        response_post = requests.post(SERVICE, json={'callback_url': "test6"})
        response_content = response_post.json()
        assert (response_post.status_code == 201)

        with open('images/test6.png', 'rb') as image_file:
            response_put_s3 = requests.put(response_content["presigned_url"], data=image_file)
            assert (response_put_s3.status_code == 200)
            time.sleep(SLEEP)
            response_get = requests.get(SERVICE + "/" + response_content["blob_id"])
            print (response_get.json())
            assert (response_get.status_code == 200)
            assert (response_get.json()["blob_id"] == response_content["blob_id"])
            assert (response_get.json()["callback_url"] == "test6")
            assert (response_get.json()["error_message"] == "An error occurred (InvalidImageFormatException) when calling the DetectLabels operation: Request has invalid image format")

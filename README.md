# BLOBS - A Simple Image Rekognition Application
This is a serverless application able to offer a service to third party applications that perform image recognition

## Steps:
* Send request with optionally provided callback_url in request body. Response return unique upload_url.
* Upload a picture to the upload_url
* Once the image recognition process finishes, you will receive a callback under the callback_url you indicated in the first step
* You can also retrieve the results from a GET endpoint

# Installation
This service needs serverless framework that is build on top of nodejs 
* Install nodejs needed by serverless: `https://nodejs.org/en/download/`
* Install serverless framework that will be used to deploy on aws cloudformation stack: `https://www.serverless.com/framework/docs/getting-started`
* Install serverless-apigateway-service-proxy plugin that will be used to proxy request directly to dynamodb: `sls plugin install -n serverless-apigateway-service-proxy`
* Install serverless-python-requirements that will be used to pack different python libs into the lambda: `sls plugin install -n serverless-python-requirements`
* Install docker for python libs required by lambdas(needed by the step above) ex: requests: `https://www.docker.com/products/docker-desktop`

# Deploy
To deploy the application into a aws account you need: `sls deploy`

# Swagger 
Check blobs-openapi.yml for documentation
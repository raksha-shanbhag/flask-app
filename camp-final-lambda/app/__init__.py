from flask import Flask
from flask_cors import CORS
import boto3
from dotenv import dotenv_values

app = Flask(__name__)
CORS(app)

# Dotenv values
config = dotenv_values(".env")

# Credentials setup
aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
aws_access_secret = config["AWS_ACCESS_SECRET_KEY"]
region_name = config["AWS_REGION"]

# Set up DynamoDB client
dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_access_secret,
                              region_name=region_name)

from app import routes
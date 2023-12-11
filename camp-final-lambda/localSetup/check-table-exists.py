import boto3
import os
from dotenv import dotenv_values


# Dotenv values
config = dotenv_values(".env")


# Credentials setup
aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
aws_access_secret = config["AWS_ACCESS_SECRET_KEY"]
region_name = config["AWS_REGION"]

dynamodb = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_access_secret,
                              region_name=region_name)

# dynamodb = boto3.client('dynamodb')

table_name = 'Camp-E2E-table'

# Use the describe_table method to check if the table exists
try:
    dynamodb.describe_table(TableName=table_name)
    print(f"The table {table_name} exists.")
except dynamodb.exceptions.ResourceNotFoundException:
    print(f"The table {table_name} does not exist.")
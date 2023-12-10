import boto3
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

table_name = 'Camp-E2E-table'
key_schema = [
    {'AttributeName': 'testConfigId', 'KeyType': 'HASH'},
    {'AttributeName': 'payloadIdOrStatus', 'KeyType': 'RANGE'}
]
attribute_definitions = [
    {'AttributeName': 'testConfigId', 'AttributeType': 'S'},
    {'AttributeName': 'payloadIdOrStatus', 'AttributeType': 'S'}
]

provisioned_throughput = {
    'ReadCapacityUnits': 5,
    'WriteCapacityUnits': 5
}

# Create the table
dynamodb.create_table(
    TableName=table_name,
    KeySchema=key_schema,
    AttributeDefinitions=attribute_definitions,
    ProvisionedThroughput=provisioned_throughput
)

print(f"Table {table_name} created.")

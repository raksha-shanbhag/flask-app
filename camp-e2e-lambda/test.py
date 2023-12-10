import boto3
from dotenv import dotenv_values
import uuid
from enum import Enum
import dbConstants as attr
from datetime import datetime
from botocore.exceptions import ClientError

TABLE_NAME = 'Camp-E2E-table'
PARTITION_KEY = 'testConfigId'
SORT_KEY = 'payloadId'
CONFIG_SORT_VALUE = 'config'

class TESTCONFIGSTATUS(Enum):
    ACTIVE = 'Active'
    ARCHIVED = 'Archived'



# Dotenv values
config = dotenv_values(".env")

# Credentials setup
aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
aws_access_secret = config["AWS_ACCESS_SECRET_KEY"]
region_name = config["AWS_REGION"]

dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_access_secret,
                              region_name=region_name)

table = dynamodb.Table(TABLE_NAME)

# get all active configurations
def get_all_active_test_configs():
    response = table.query(
        FilterExpression='#payloadId = :payloadId AND #status = :status', 
        ExpressionAttributeNames={
            '#payloadId': attr.SORT_KEY,
            '#status': attr.COL_STATUS
        },
        ExpressionAttributeValues={
            ':payloadId': CONFIG_SORT_VALUE,
            ':status': TESTCONFIGSTATUS.ACTIVE.value
        }
    )
    return response["Items"]
    


# # Print the results
# def get_all_test_configs(testConfigId, name, description, productIdMapping, brandIdMapping, creditPolicyId, mensaFileName, csvData):
#     # Define the item to be added to the table
#     current_time = datetime.utcnow().isoformat()

#     # update table
#     key = {
#         attr.PARTITION_KEY: test_uuid,
#         attr.SORT_KEY: CONFIG_SORT_VALUE # payloadId = 'config'
#     }

#     # update_expression = 'SET #name = :name, #description = :description, #productIdMapping = :productIdMapping, #brandIdMapping = :brandIdMapping '
#     # update_expression += '#mensaFileName = :mensaFileName, #csvData = :csvData, #creditPolicyId = :creditPolicyId, #lastUpdated = :lastUpdated'
        

#     update_expression = f'SET {attr.COL_NAME} = :name, {attr.COL_DESCRIPTION} = :description, {attr.COL_PRODID_MAPPING} = :productIdMapping, {attr.COL_BRANDID_MAPPING} = :brandIdMapping, '
#     update_expression += f'{attr.COL_MENSAFILENAME} = :mensaFileName, {attr.COL_CSV_DATA} = :csvData, {attr.COL_CREDITPOLICYID} = :creditPolicyId, {attr.COL_LAST_UPDATED} = :lastUpdated'
    
#     condition_expression = f'attribute_exists({attr.PARTITION_KEY}) AND attribute_exists({attr.SORT_KEY})'

#     # expression_attribute_names = {
#     #     '#name': attr.COL_NAME,
#     #     '#description': attr.COL_DESCRIPTION,
#     #     '#productIdMapping': attr.COL_PRODID_MAPPING,
#     #     '#brandIdMapping': attr.COL_BRANDID_MAPPING,
#     #     '#creditPolicyId': attr.COL_CREDITPOLICYID,
#     #     '#mensaFileName': attr.COL_MENSAFILENAME,
#     #     '#csvData': attr.COL_CSV_DATA,
#     #     '#lastUpdated': attr.COL_LAST_UPDATED
#     # }
    
#     expression_attribute_values = {
#         ':name': name,
#         ':description': description,
#         ':productIdMapping': productIdMapping,
#         ':brandIdMapping': brandIdMapping,
#         ':creditPolicyId': creditPolicyId,
#         ':mensaFileName': mensaFileName,
#         ':csvData': csvData,
#         ':lastUpdated': current_time
#     }

#     # get response
#     try:
#         response = table.update_item(
#             Key=key,
#             UpdateExpression=update_expression,
#             # ExpressionAttributeNames=expression_attribute_names,
#             ExpressionAttributeValues=expression_attribute_values,
#             ReturnValues='ALL_NEW',
#             ConditionExpression=condition_expression,
#         )
#     # except ClientError as e:
#     #     if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
#     #         # Handle condition check failure
#     #         print("Condition check failed. The item may not exist.")
#     #     else:
#     #         # Handle other exceptions (e.g., database errors)
#     #         print("Error:", e)
#     except Exception as e:
#         if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
#             # Handle condition check failure
#             print("Condition check failed. The item may not exist.")
#         else:
#             # Handle other exceptions (e.g., database errors)
#             print("Error:", e.response['Error']['Code'])
#         return e


#     return response

def create_test_config(name, description, productIdMapping, brandIdMapping, creditPolicyId, mensaFileName, csvData):
    unique_id = str(uuid.uuid4())
    current_time = datetime.utcnow().isoformat()
    
    item = {
        attr.PARTITION_KEY: unique_id, # testConfigId
        attr.SORT_KEY: TESTCONFIGSTATUS.ACTIVE.value, # payloadId = 'Active'
        attr.COL_NAME: name,
        attr.COL_DESCRIPTION: description,
        attr.COL_BRANDID_MAPPING: brandIdMapping,
        attr.COL_PRODID_MAPPING: productIdMapping,
        attr.COL_CREDITPOLICYID: creditPolicyId,
        attr.COL_MENSAFILENAME: mensaFileName,
        attr.COL_CSV_DATA: csvData,
        attr.COL_DATE_CREATED: current_time,
        attr.COL_LAST_UPDATED: current_time
    }

    # Put the item into the table
    response = table.put_item(Item=item)
    return response

test_uuid = '7cc3fffa-5971-4a65-85bc-173ad'
name = "3eddde444-Raksddha"
description = "Redddsss"
productIdMapping = "{e33ndwqdqwwqqwednudnn: dusooj}"
brandIdMapping = "{e22222ewww:Wwee}"
creditPolicyId= 23222939
mensaFileName = "dijodsddsjiodsj"
csvData = [['test_caseId', 'test_name'], [522, 'Rakddsdsha'], [17822, 'Rakddsdsha']]

# response = get_all_test_configs(test_uuid, name, description, productIdMapping, brandIdMapping, creditPolicyId, mensaFileName, csvData)                             
# response = create_test_config(name, description, productIdMapping, brandIdMapping, creditPolicyId, mensaFileName, csvData)
# print(response)


def get_all_active_test_configs1():
    response = table.scan(
        FilterExpression=f'{attr.SORT_KEY} = :payload_id',
        ExpressionAttributeValues = {
            ':payload_id': TESTCONFIGSTATUS.ACTIVE.value
        }
    )
    return response["Items"]
# print(resp)







# response = self.table.query(
#     KeyConditionExpression='testConfigId = :testConfigId AND payloadId = :payloadId',
#     ExpressionAttributeValues={
#         ':testConfigId': testConfigId,
#         ':payloadId': 'config'
#     }
# )



# # response = dynamodb.meta.client.describe_table(TableName=TABLE_NAME)

# # print("Table Schema:", response['Table']['KeySchema'])
# # for item in items:
# #     print(item)






# class TESTCONFIGSTATUS(Enum):
#     ACTIVE = 'Active'
#     ARCHIVED = 'Archived'
#     DELETED = 'Deleted'

# print(TESTCONFIGSTATUS.ACTIVE.value)
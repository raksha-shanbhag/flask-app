import dbConstants as attr
from dbConstants import CONFIG_SORT_VALUE, TESTCONFIGSTATUS, TABLE_NAME
import app.repository.utilities as utilities

class TestConfigRepository:
    def __init__(self, dynamodb):
        self.table = dynamodb.Table(TABLE_NAME)
    
    # get all active configurations
    def get_all_active_test_configs(self):
        response = self.table.scan(
            FilterExpression=f'{attr.SORT_KEY} = :payload_id',
            ExpressionAttributeValues = {
                ':payload_id': TESTCONFIGSTATUS.ACTIVE.value
            }
        )
        return response["Items"]
    
    # get all archived configurations
    def get_all_archived_test_configs(self):
        response = self.table.query(
            FilterExpression=f'{attr.SORT_KEY} = :payload_id',
            ExpressionAttributeValues = {
                ':payload_id': TESTCONFIGSTATUS.ARCHIVED.value
            }
        )
        return response["Items"]

    # get test config by Id
    def get_test_config_by_id(self, testConfigId, status):
        key = {
            attr.PARTITION_KEY: testConfigId,
            attr.SORT_KEY: status
        }
        response = self.table.get_item(
            Key = key
        )
        return response["Item"]
            

    # create a test config
    def create_test_config(self, name, description, productIdMapping, brandIdMapping, creditPolicyId, mensaFileName, csvData):
        unique_id = utilities.get_uuid()
        current_time = utilities.get_datenow_iso()
        
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
        response = self.table.put_item(Item=item)
        return item
    
    # edit test configuration
    def edit_test_configuration(self, testConfigId, name, description, productIdMapping, brandIdMapping, creditPolicyId, mensaFileName, csvData):
        current_time = utilities.get_datenow_iso()

        # update table
        key = {
            attr.PARTITION_KEY: testConfigId,
            attr.SORT_KEY: TESTCONFIGSTATUS.ACTIVE.value # payloadId = 'Active' only active configurations
        }

        update_expression = 'SET #name = :name, #description = :description, #productIdMapping = :productIdMapping, #brandIdMapping = :brandIdMapping, #mensaFileName = :mensaFileName, #csvData = :csvData, #creditPolicyId = :creditPolicyId, #lastUpdated = :lastUpdated'
        condition_expression = 'attribute_exists(#testConfigId) AND attribute_exists(#payloadIdOrStatus)'

        expression_attribute_names = {
            '#testConfigId': attr.PARTITION_KEY,
            '#payloadIdOrStatus': attr.SORT_KEY,
            '#name': attr.COL_NAME,
            '#description': attr.COL_DESCRIPTION,
            '#productIdMapping': attr.COL_PRODID_MAPPING,
            '#brandIdMapping': attr.COL_BRANDID_MAPPING,
            '#creditPolicyId': attr.COL_CREDITPOLICYID,
            '#mensaFileName': attr.COL_MENSAFILENAME,
            '#csvData': attr.COL_CSV_DATA,
            '#lastUpdated': attr.COL_LAST_UPDATED
        }

        expression_attribute_values = {
            ':name': name,
            ':description': description,
            ':productIdMapping': productIdMapping,
            ':brandIdMapping': brandIdMapping,
            ':creditPolicyId': creditPolicyId,
            ':mensaFileName': mensaFileName,
            ':csvData': csvData,
            ':lastUpdated': current_time
        }

        # get response
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW' 
        )
        return response['Item']

    # delete test configuration
    def delete_test_configuration(self, testConfigId):
        # scan for testConfig and test results
        response = self.table.scan(
            FilterExpression='#testConfigId = :testConfigId',
            ExpressionAttributeNames={'#testConfigId': attr.PARTITION_KEY},
            ExpressionAttributeValues={':testConfigId': testConfigId}
        )

        # delete all records with testConfigId 
        for item in response['Items']:
            key = {
                attr.PARTITION_KEY: testConfigId,
                attr.SORT_KEY: item[attr.SORT_KEY] #payloadIdOrStatus
            }
            self.table.delete_item(Key = key)
    
    # archive test configuration
    def archive_test_configuration(self, testConfigId):
        key = {
            attr.PARTITION_KEY: testConfigId,
            attr.SORT_KEY: TESTCONFIGSTATUS.ACTIVE.value # payloadIdOrStatus = 'ACTIVE'
        }

        update_expression = 'SET #payloadIdOrStatus= :status'
        condition_expression = 'attribute_exists(#testConfigId) AND attribute_exists(#payloadIdOrStatus)'

        expression_attribute_names = {
            '#testConfigId': attr.PARTITION_KEY,
            '#payloadIdOrStatus': attr.SORT_KEY
        }

        expression_attribute_values = {
            ':status': TESTCONFIGSTATUS.ARCHIVED.value
        }

        # get response
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW' 
        )
        return response['Item']
    
    # unarchive test configuration
    def unarchive_test_configuration(self, testConfigId):
        key = {
            attr.PARTITION_KEY: testConfigId,
            attr.SORT_KEY: TESTCONFIGSTATUS.ARCHIVED.value # payloadIdOrStatus = 'ARCHIVED'
        }

        update_expression = 'SET #payloadIdOrStatus= :status'
        condition_expression = 'attribute_exists(#testConfigId) AND attribute_exists(#payloadIdOrStatus)'

        expression_attribute_names = {
            '#testConfigId': attr.PARTITION_KEY,
            '#payloadIdOrStatus': attr.SORT_KEY
        }

        expression_attribute_values = {
            ':status': TESTCONFIGSTATUS.ACTIVE.value
        }

        # get response
        response = self.table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='ALL_NEW' 
        )
        return response['Item']
import app.utilities.dbConstants as attr
from app.utilities.dbConstants import CONFIG_SORT_VALUE, TESTCONFIGSTATUS, TABLE_NAME
import app.utilities.utilities as utilities
from app.utilities.exception_handler import ConditionalException

class TestResultsRepository:
    def __init__(self, dynamodb):
      self.table = dynamodb.Table(TABLE_NAME)

    # get all test results given a testConfig Id
    def get_all_test_results(self, testConfigId):
      response = self.table.scan(
        FilterExpression='#testConfigId = :testConfigId and #payloadId <> :config',
        ExpressionAttributeNames = {
          '#testConfigId': attr.PARTITION_KEY,
          '#payloadId': attr.SORT_KEY
        },
        ExpressionAttributeValues={
          ':testConfigId': testConfigId,
          ':config': CONFIG_SORT_VALUE
        }
      )
      return response['Items']
    
    # get individual test config given a testConfig id and payloadId
    def get_test_result(self, testConfigId, payloadId):
      key = {
          attr.PARTITION_KEY: testConfigId,
          attr.SORT_KEY: payloadId
      }
      response = self.table.get_item(
          Key = key
      )
      return response["Item"]
    
    # create a test result
    def create_or_update_test_result(self, testConfigId, payloadId, result, applicationId, payload, otherFields):
      current_time = utilities.get_datenow_iso()
      
      update_expression = 'SET #result = :result, #applicationId = :applicationId, #payload = :payload, #otherFields= :otherFields, #lastUpdated = :currentTime, #dateCreated = if_not_exists(#dateCreated, :currentTime)'
      
      expression_attribute_names = {
        '#result': attr.COL_RESULT,
        '#payload': attr.COL_PAYLOAD,
        '#applicationId': attr.COL_APPLICATION_ID,
        '#otherFields': attr.COL_OTHERS,
        '#lastUpdated': attr.COL_LAST_UPDATED,
        '#dateCreated': attr.COL_DATE_CREATED
      }

      expression_attribute_values = {
        ':result': result,
        ':applicationId': applicationId,
        ':payload': payload,
        ':otherFields': otherFields,
        ':currentTime': current_time
      }

      # Put the item into the table
      return self.table.update_item(
        Key={
          attr.PARTITION_KEY: testConfigId,
          attr.SORT_KEY: payloadId
        },
        UpdateExpression=update_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
      )
    
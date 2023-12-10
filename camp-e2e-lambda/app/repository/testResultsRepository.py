import boto3
import dbConstants

class TestResultsRepository:
    def __init__(self, dynamodb):
      self.table = dynamodb.Table(dbConstants.TABLE_NAME)

    def get_all_test_configs(self):
      response = self.table.query(
          KeyConditionExpression='testConfig = :config_partition_key AND begins_with(payloadId, :payload_prefix)',
          ExpressionAttributeValues={
              ':config_partition_key': dbConstants.PARTITION_KEY,
              ':payload_prefix': dbConstants.SORT_KEY
          }
      )
      return response['Items']
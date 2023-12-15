import pytest
from unittest.mock import Mock, ANY, call
from app.repository.testConfigRepository import TestConfigRepository
from app.utilities.exception_handler import MissingResourceException
from app.utilities.dbConstants import TABLE_NAME, SORT_KEY, COL_STATUS, TESTCONFIGSTATUS, CONFIG_SORT_VALUE, PARTITION_KEY, COL_DESCRIPTION, COL_MENSAFILENAME
from app.utilities.dbConstants import COL_BRANDID_MAPPING, COL_CREDITPOLICYID, COL_CSV_DATA, COL_DATE_CREATED, COL_LAST_UPDATED, COL_NAME, COL_PRODID_MAPPING

@pytest.fixture
def dynamodb_mock():
    return Mock()

@pytest.fixture
def test_config_repo(dynamodb_mock):
    return TestConfigRepository(dynamodb_mock)

def test_get_all_active_test_configs(test_config_repo, dynamodb_mock):
    dynamodb_mock.Table.return_value.scan.return_value = {'Items': [{'status': 'value1', 'lastUpdated': '2023-01-05T12:00:00'}, {'status': 'value2', 'lastUpdated': '2023-01-02T12:00:00'}]}
    
    result = test_config_repo.get_all_active_test_configs()

    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.scan.assert_called_once_with(
        FilterExpression='#payloadId = :payload_id and #status= :status',
        ExpressionAttributeNames={'#payloadId': SORT_KEY, '#status': COL_STATUS },
        ExpressionAttributeValues={':payload_id': CONFIG_SORT_VALUE, ':status': TESTCONFIGSTATUS.ACTIVE.value}
    )
    assert result == [{'status': 'value2', 'lastUpdated': '2023-01-02T12:00:00'}, {'status': 'value1', 'lastUpdated': '2023-01-05T12:00:00'}]

def test_get_all_archived_test_configs(test_config_repo, dynamodb_mock):
    dynamodb_mock.Table.return_value.scan.return_value = {'Items': [{'status': 'value1', 'lastUpdated': '2023-01-05T12:00:00'}, {'status': 'value2', 'lastUpdated': '2023-01-02T12:00:00'}]}
    
    result = test_config_repo.get_all_archived_test_configs()

    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.scan.assert_called_once_with(
        FilterExpression='#payloadId = :payload_id and #status= :status',
        ExpressionAttributeNames={'#payloadId': SORT_KEY, '#status': COL_STATUS },
        ExpressionAttributeValues={':payload_id': CONFIG_SORT_VALUE, ':status': TESTCONFIGSTATUS.ARCHIVED.value}
    )
    assert result == [{'status': 'value2', 'lastUpdated': '2023-01-02T12:00:00'}, {'status': 'value1', 'lastUpdated': '2023-01-05T12:00:00'}]

def test_get_test_config_by_id(test_config_repo, dynamodb_mock):
    # Mock response from DynamoDB
    expected_response = {PARTITION_KEY: "3", SORT_KEY: CONFIG_SORT_VALUE, "attr2": "value2", "lastUpdated": "2023-01-01T12:00:00"}
    dynamodb_mock.Table.return_value.get_item.return_value = {"Item": expected_response}
    
    # Call the method with a testConfigId
    result = test_config_repo.get_test_config_by_id("3")

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.get_item.assert_called_once_with(
        Key={PARTITION_KEY : "3",  SORT_KEY: expected_response[SORT_KEY]}
    )

    # Assert the result matches the expected response
    assert result == expected_response

def test_archive_test_configuration(test_config_repo, dynamodb_mock):
    # Mock response from DynamoDB update_item
    expected_response = {PARTITION_KEY: "3", SORT_KEY: CONFIG_SORT_VALUE, "attr2": "value2", "lastUpdated": "2023-01-01T12:00:00"}
    dynamodb_mock.Table.return_value.update_item.return_value = expected_response

    # Call the method with a testConfigId
    result = test_config_repo.archive_test_configuration("3")

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.update_item.assert_called_once_with(
        Key={PARTITION_KEY : "3",  SORT_KEY: expected_response[SORT_KEY]},
        UpdateExpression='SET #status= :status',
        ConditionExpression='attribute_exists(#testConfigId) AND attribute_exists(#payloadId)',
        ExpressionAttributeNames={'#testConfigId': PARTITION_KEY, '#payloadId': SORT_KEY, '#status': COL_STATUS},
        ExpressionAttributeValues={':status': TESTCONFIGSTATUS.ARCHIVED.value},
        ReturnValues='ALL_NEW'
    )

    # Assert the result matches the expected response
    assert result == expected_response

def test_unarchive_test_configuration(test_config_repo, dynamodb_mock):
    # Mock response from DynamoDB update_item
    expected_response = {PARTITION_KEY: "3", SORT_KEY: CONFIG_SORT_VALUE, "attr2": "value2", "lastUpdated": "2023-01-01T12:00:00"}
    dynamodb_mock.Table.return_value.update_item.return_value = expected_response

    # Call the method with a testConfigId
    result = test_config_repo.unarchive_test_configuration("3")

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.update_item.assert_called_once_with(
        Key={PARTITION_KEY : "3",  SORT_KEY: expected_response[SORT_KEY]},
        UpdateExpression='SET #status= :status',
        ConditionExpression='attribute_exists(#testConfigId) AND attribute_exists(#payloadId)',
        ExpressionAttributeNames={'#testConfigId': PARTITION_KEY, '#payloadId': SORT_KEY, '#status': COL_STATUS},
        ExpressionAttributeValues={':status': TESTCONFIGSTATUS.ACTIVE.value},
        ReturnValues='ALL_NEW'
    )

    # Assert the result matches 
    assert result == expected_response

def test_create_test_config(test_config_repo, dynamodb_mock):
    # Mock response from DynamoDB put_item
    item = {
        PARTITION_KEY: ANY, # testConfigId
        SORT_KEY: CONFIG_SORT_VALUE, # payloadId = 'config'
        COL_NAME: 'name',
        COL_DESCRIPTION: 'description',
        COL_STATUS: TESTCONFIGSTATUS.ACTIVE.value,
        COL_BRANDID_MAPPING: 'brandIdMapping',
        COL_PRODID_MAPPING: 'productIdMapping',
        COL_CREDITPOLICYID: 'creditPolicyId',
        COL_MENSAFILENAME: 'mensaFileName',
        COL_CSV_DATA: ['csvData'],
        COL_DATE_CREATED: ANY,
        COL_LAST_UPDATED: ANY
    }
    dynamodb_mock.Table.return_value.put_item.return_value = item

    # Call the method with data
    result = test_config_repo.create_test_config("name", "description", "productIdMapping", "brandIdMapping", "creditPolicyId", "mensaFileName", ["csvData"])

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.put_item.assert_called_once_with(
        Item=item
    )

    # Assert the result matches the expected response
    assert result == item


def test_edit_test_configuration(test_config_repo, dynamodb_mock):
    # Mock response from DynamoDB update_item
    expected_response = {
        PARTITION_KEY: ANY,  # testConfigId
        SORT_KEY: CONFIG_SORT_VALUE,  # payloadId = 'config'
        COL_NAME: 'UpdatedName',
        COL_DESCRIPTION: 'UpdatedDescription',
        COL_STATUS: TESTCONFIGSTATUS.ACTIVE.value,
        COL_BRANDID_MAPPING: 'UpdatedBrandIdMapping',
        COL_PRODID_MAPPING: 'UpdatedProductIdMapping',
        COL_CREDITPOLICYID: 'UpdatedCreditPolicyId',
        COL_MENSAFILENAME: 'UpdatedMensaFileName',
        COL_CSV_DATA: 'UpdatedCsvData',
        COL_DATE_CREATED: ANY,
        COL_LAST_UPDATED: ANY
    }
    dynamodb_mock.Table.return_value.update_item.return_value = expected_response

    # Call the method with data
    result = test_config_repo.edit_test_configuration("TestConfigId", "UpdatedName", "UpdatedDescription", "UpdatedProductIdMapping", "UpdatedBrandIdMapping", "UpdatedCreditPolicyId", "UpdatedMensaFileName", "UpdatedCsvData")

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.update_item.assert_called_once_with(
        Key={ PARTITION_KEY : "TestConfigId",  SORT_KEY: CONFIG_SORT_VALUE},
        UpdateExpression='SET #name = :name, #description = :description, #productIdMapping = :productIdMapping, #brandIdMapping = :brandIdMapping, #mensaFileName = :mensaFileName, #csvData = :csvData, #creditPolicyId = :creditPolicyId, #lastUpdated = :lastUpdated',
        ConditionExpression='attribute_exists(#testConfigId) AND attribute_exists(#payloadId)',
        ExpressionAttributeNames={
            '#testConfigId': PARTITION_KEY,
            '#payloadId': SORT_KEY,
            '#name': COL_NAME,
            '#description': COL_DESCRIPTION,
            '#productIdMapping': COL_PRODID_MAPPING,
            '#brandIdMapping': COL_BRANDID_MAPPING,
            '#creditPolicyId': COL_CREDITPOLICYID,
            '#mensaFileName': COL_MENSAFILENAME,
            '#csvData': COL_CSV_DATA,
            '#lastUpdated': COL_LAST_UPDATED,
        },
        ExpressionAttributeValues={
            ':name': 'UpdatedName',
            ':description': 'UpdatedDescription',
            ':productIdMapping': 'UpdatedProductIdMapping',
            ':brandIdMapping': 'UpdatedBrandIdMapping',
            ':creditPolicyId': 'UpdatedCreditPolicyId',
            ':mensaFileName': 'UpdatedMensaFileName',
            ':csvData': 'UpdatedCsvData',
            ':lastUpdated': ANY,
        },
        ReturnValues='ALL_NEW'
    )

    # Assert the result matches the expected response
    assert result == expected_response

def test_delete_test_configuration_with_items(test_config_repo, dynamodb_mock):
    # Mock response from DynamoDB scan
    dynamodb_mock.Table.return_value.scan.return_value = {'Items': [{PARTITION_KEY: 'testConfigId', SORT_KEY: 'value1'}, {PARTITION_KEY: 'testConfigId', SORT_KEY: 'value2'}]}

    # Call the method with data
    test_config_repo.delete_test_configuration('testConfigId')

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.scan.assert_called_once_with(
        FilterExpression='#testConfigId = :testConfigId',
        ExpressionAttributeNames={'#testConfigId': PARTITION_KEY},
        ExpressionAttributeValues={':testConfigId': 'testConfigId'}
    )
    dynamodb_mock.Table.return_value.delete_item.assert_has_calls([
        call(Key={PARTITION_KEY: 'testConfigId', SORT_KEY: 'value1'}),
        call(Key={PARTITION_KEY: 'testConfigId', SORT_KEY: 'value2'})
    ])

def test_delete_test_configuration_no_items(test_config_repo, dynamodb_mock):
    # Mock response from DynamoDB scan with no items
    dynamodb_mock.Table.return_value.scan.return_value = {'Items': []}

    # Call the method with data
    with pytest.raises(MissingResourceException):
        test_config_repo.delete_test_configuration('testConfigId')

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.scan.assert_called_once_with(
        FilterExpression='#testConfigId = :testConfigId',
        ExpressionAttributeNames={'#testConfigId': PARTITION_KEY},
        ExpressionAttributeValues={':testConfigId': 'testConfigId'}
    )
    assert not dynamodb_mock.Table.return_value.delete_item.called
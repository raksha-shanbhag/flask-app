import pytest
from unittest.mock import Mock, ANY
from app.repository.testResultsRepository import TestResultsRepository
from app.utilities.dbConstants import PARTITION_KEY, SORT_KEY, TABLE_NAME, CONFIG_SORT_VALUE, COL_LAST_UPDATED
from app.utilities.dbConstants import COL_OTHERS, COL_PAYLOAD, COL_APPLICATION_ID, COL_DATE_CREATED, COL_RESULT


@pytest.fixture
def dynamodb_mock():
    return Mock()

@pytest.fixture
def test_results_repo(dynamodb_mock):
    return TestResultsRepository(dynamodb_mock)

def test_get_all_test_results(test_results_repo, dynamodb_mock):
    # Mock response from DynamoDB scan
    expected_response = [{'attr1': 'value1'}, {'attr2': 'value2'}]
    dynamodb_mock.Table.return_value.scan.return_value = {'Items': expected_response}

    # Call the method with data
    result = test_results_repo.get_all_test_results('testConfigId')

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.scan.assert_called_once_with(
        FilterExpression='#testConfigId = :testConfigId and #payloadId <> :config',
        ExpressionAttributeNames={
            '#testConfigId': PARTITION_KEY,
            '#payloadId': SORT_KEY
        },
        ExpressionAttributeValues={
            ':testConfigId': 'testConfigId',
            ':config': CONFIG_SORT_VALUE
        }
    )

    # Assert the result matches the expected response
    assert result == expected_response


def test_get_test_result(test_results_repo, dynamodb_mock):
    # Mock response from DynamoDB get_item
    expected_response = {"attr1": "value1", "attr2": "value2"}
    dynamodb_mock.Table.return_value.get_item.return_value = {'Item': expected_response}

    # Call the method with data
    result = test_results_repo.get_test_result('testConfigId', 'payloadId')

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.get_item.assert_called_once_with(
        Key={
            PARTITION_KEY: 'testConfigId',
            SORT_KEY: 'payloadId'
        }
    )

    # Assert the result matches the expected response
    assert result == expected_response

def test_get_test_result_not_found(test_results_repo, dynamodb_mock):
    # Mock response from DynamoDB get_item with no item found
    dynamodb_mock.Table.return_value.get_item.return_value = {'Item': None}

    # Call the method with data
    result = test_results_repo.get_test_result('testConfigId', 'payloadId')

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.get_item.assert_called_once_with(
        Key={
            PARTITION_KEY: 'testConfigId',
            SORT_KEY: 'payloadId'
        }
    )

    # Assert the result is None when item is not found
    assert result is None


def test_create_or_update_test_result(test_results_repo, dynamodb_mock):
    # Mock response from DynamoDB update_item
    expected_response = {"attr1": "value1", "attr2": "value2"}
    dynamodb_mock.Table.return_value.update_item.return_value = {'Attributes': expected_response}

    # Call the method with data
    result = test_results_repo.create_or_update_test_result(
        'testConfigId', 'payloadId', 'result', 'applicationId', 'payload', {'field1': 'value1'}
    )

    # Assert the DynamoDB method was called with the correct parameters
    dynamodb_mock.Table.assert_called_once_with(TABLE_NAME)
    dynamodb_mock.Table.return_value.update_item.assert_called_once_with(
        Key={
            PARTITION_KEY: 'testConfigId',
            SORT_KEY: 'payloadId'
        },
        UpdateExpression='SET #result = :result, #applicationId = :applicationId, #payload = :payload, #otherFields= :otherFields, #lastUpdated = :currentTime, #dateCreated = if_not_exists(#dateCreated, :currentTime)',
        ExpressionAttributeNames={
            '#result': COL_RESULT,
            '#applicationId': COL_APPLICATION_ID,
            '#payload': COL_PAYLOAD,
            '#otherFields': COL_OTHERS,
            '#lastUpdated': COL_LAST_UPDATED,
            '#dateCreated': COL_DATE_CREATED,
        },
        ExpressionAttributeValues={
            ':result': 'result',
            ':applicationId': 'applicationId',
            ':payload': 'payload',
            ':otherFields': {'field1': 'value1'},
            ':currentTime': ANY,
        },
        ReturnValues='ALL_NEW'
    )
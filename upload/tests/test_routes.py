import json
import pytest
from unittest.mock import Mock, patch
from app import app
from app.repository.testConfigRepository import TestConfigRepository

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.routes.TestConfigRepo')
def test_get_all_test_configs(test_config_rep, client):
    # Mock the response from TestConfigRepository
    test_config_rep.get_all_active_test_configs.return_value = [
        {"config_key": "value1", "last_updated": 1},
        {"config_key": "value2", "last_updated": 2}
    ]

    # Make a request to the route
    response = client.get('/testConfigs')

    # Ensure that the TestConfigRepository method was called
    test_config_rep.get_all_active_test_configs.assert_called_once()

    # Check the response
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']) == 2


@patch('app.routes.TestConfigRepo')
def test_get_all_archived_test_configs(test_config_rep, client):
    # Mock the response from TestConfigRepository
    test_config_rep.get_all_archived_test_configs.return_value = [
        {"config_key": "value1", "last_updated": 1},
        {"config_key": "value2", "last_updated": 2}
    ]

    # Make a request to the route
    response = client.get('/testConfigs/archived')

    # Ensure that the TestConfigRepository method was called
    test_config_rep.get_all_archived_test_configs.assert_called_once()

    # Check the response
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']) == 2


@patch('app.routes.TestResultsRepo')
def test_get_all_test_results_for_config(mock_test_results_repo, client):
    # Mock the response from TestResultsRepository
    mock_test_results_repo.get_all_test_results.return_value = [
        {"result_key": "value1", "timestamp": 1},
        {"result_key": "value2", "timestamp": 2}
    ]

    # Make a request to the route with a specific testConfigId
    test_config_id = "some_test_config_id"
    response = client.get(f'/testResults/{test_config_id}')

    # Ensure that the TestResultsRepository method was called with the correct testConfigId
    mock_test_results_repo.get_all_test_results.assert_called_once_with(test_config_id)

    # Check the response
    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']) == 2
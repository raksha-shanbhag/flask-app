from app import app, dynamodb
from app.repository.testConfigRepository import TestConfigRepository
from app.repository.testResultsRepository import TestResultsRepository
from flask import jsonify, request

TestResultsRepo = TestResultsRepository(dynamodb)
TestConfigRepo = TestConfigRepository(dynamodb)

###### Test configuration routes
# Get all active test configurations
@app.route('/testConfigs', methods=['GET'])
def get_all_test_configs():
    data = {}
    try:
        data = TestConfigRepo.get_all_active_test_configs()
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 'error', 'message': error_message}), 500
    return jsonify({'status': 'success', 'data': data}), 200

# Get all archived test configurations
@app.route('/testConfigs/archived', methods=['GET'])
def get_all_archived_test_configs():
    data = {}
    try:
        data = TestConfigRepo.get_all_archived_test_configs()
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 'error', 'message': error_message}), 500
    return jsonify({'status': 'success', 'data': data}), 200


# Create a test Config
@app.route('/testConfigs', methods=['POST'])
def create_test_configs():
    request_data = request.get_json()
    try:
        data = TestConfigRepository.create_test_config()
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 'error', 'message': error_message}), 500
    return jsonify({'status': 'success', 'data': data}), 200

# Edit a test Configuration
@app.route('/testConfigs/:testConfigId', method=['PUT'])
def index():
    request_data = request.get_json()
    try:
        data = TestConfigRepository.create_test_config()
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 'error', 'message': error_message}), 500
    return jsonify({'status': 'success', 'data': data}), 200

# Archive a test configuration
@app.route('/testConfigs/:testConfigId/archive', method=['PUT'])
def index():
    request_data = request.get_json()
    try:
        data = TestConfigRepository.create_test_config()
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 'error', 'message': error_message}), 500
    return jsonify({'status': 'success', 'data': data}), 200

# Unarchive a test configuration
@app.route('/testConfigs/:testConfigId/unarchive', method=['PUT'])
def index():
    request_data = request.get_json()
    try:
        data = TestConfigRepository.create_test_config()
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 'error', 'message': error_message}), 500
    return jsonify({'status': 'success', 'data': data}), 200

# Delete a test Configuration
@app.route('/testConfigs/:testConfigId', method=['DELETE'])
def delete_test_configuration():
    request_data = request.get_json()
    try:
        data = TestConfigRepository.create_test_config()
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 'error', 'message': error_message}), 500
    return jsonify({'status': 'success', 'data': data}), 200




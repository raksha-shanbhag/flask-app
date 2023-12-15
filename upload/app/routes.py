from app import app, dynamodb
from app.repository.testConfigRepository import TestConfigRepository
from app.repository.testResultsRepository import TestResultsRepository
from flask import jsonify, request
from app.utilities.exception_handler import handle_exception
import json

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
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

# Get all archived test configurations
@app.route('/testConfigs/archived', methods=['GET'])
def get_all_archived_test_configs():
    data = {}
    try:
        data = TestConfigRepo.get_all_archived_test_configs()
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200


# Create a test Config
@app.route('/testConfigs', methods=['POST'])
def create_test_configs():
    try:
        request_data = request.get_json()
        data = TestConfigRepo.create_test_config(
            name= request_data['name'],
            description= request_data['description'],
            productIdMapping= request_data['productIdMapping'],
            brandIdMapping= request_data['brandIdMapping'],
            creditPolicyId= request_data['creditPolicyId'],
            mensaFileName= request_data['mensaFileName'],
            csvData= json.loads(request_data['csvData'])
        )
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

# Edit a test Configuration
@app.route('/testConfigs/<testConfigId>', methods=['PUT'])
def edit_test_configuration(testConfigId):
    try:
        request_data = request.get_json()
        data = TestConfigRepo.edit_test_configuration(
            testConfigId= testConfigId,
            name= request_data['name'],
            description= request_data['description'],
            productIdMapping= request_data['productIdMapping'],
            brandIdMapping= request_data['brandIdMapping'],
            creditPolicyId= request_data['creditPolicyId'],
            mensaFileName= request_data['mensaFileName'],
            csvData= json.loads(request_data['csvData'])
        )
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

# Archive a test configuration
@app.route('/testConfigs/<testConfigId>/archive', methods=['PUT'])
def archive_test_configuration(testConfigId):
    try:
        data = TestConfigRepo.archive_test_configuration(testConfigId)
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

# Unarchive a test configuration
@app.route('/testConfigs/<testConfigId>/unarchive', methods=['PUT'])
def unarchive_test_configuration(testConfigId):
    try:
        data = TestConfigRepo.unarchive_test_configuration(testConfigId)
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

# Delete a test Configuration
@app.route('/testConfigs/<testConfigId>', methods=['DELETE'])
def delete_test_configuration(testConfigId):
    try:
        data = TestConfigRepo.delete_test_configuration(testConfigId)
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

###### Test Results routes
# Get all test Results
@app.route('/testResults/<testConfigId>', methods=['GET'])
def get_all_test_results_for_config(testConfigId):
    try:
        data = TestResultsRepo.get_all_test_results(testConfigId)
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

# Get a test Result
@app.route('/testResults/<testConfigId>/payload/<payloadId>', methods=['GET'])
def get_test_result_for_config(testConfigId, payloadId):
    try:
        data = TestResultsRepo.get_test_result(testConfigId=testConfigId, payloadId=payloadId)
    except Exception as e:
        return handle_exception(e)
    return jsonify({'status': 'success', 'data': data}), 200

# # Run tests for a config
# @app.route('/runTests/<testConfigId>', methods=['GET'])
# def run_all_tests(testConfig):
#     try:
#         data = ''
#     except Exception as e:
#         return handle_exception(e)
#     return jsonify({'status': 'success', 'data': data}), 200

# # Run particular test
# @app.route('/runTests/<testConfigId>/payloadId/<payloadId>', methods=['GET'])
# def run_individual_test(testConfig, payloadId):
#     try:
#         data = ''
#     except Exception as e:
#         return handle_exception(e)
#     return jsonify({'status': 'success', 'data': data}), 200
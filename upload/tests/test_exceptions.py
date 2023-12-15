import pytest
from flask import Flask, jsonify
import json
from app.utilities.exception_handler import handle_exception, MissingResourceException

@pytest.fixture
def app():
    return Flask(__name__)

# def test_handle_exception_resource_not_found(app):
#     with app.app_context():
#         # Simulate a ConditionalCheckFailedException
#         exception = CustomConditionalException({ 'response': {'Error': {'Code': 'ConditionalCheckFailedException'}}})
#         response_json, status_code = handle_exception(exception)
#         expected_json = {'status': 'error', 'message': 'Resource Not found'}
#         # assert response_json == expected_json
#         assert status_code == 500


def test_handle_exception_resource_not_found(app):
    with app.app_context():
        # Create a ConditionalException with the required structure
        exception = MissingResourceException()

        # Call the handle_exception function
        response, status_code = handle_exception(exception)

        # Assert the expected response and status code
        expected_response = {'status': 'error', 'message': 'Resource Not found'}
        assert response.json == expected_response
        assert status_code == 404

def test_handle_exception_general_exception(app):
    with app.app_context():
        with pytest.raises(Exception) as che:
            k = 1/0
        code, ans = handle_exception(che)

        assert ans == 500
        
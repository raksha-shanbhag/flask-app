from flask import jsonify

class ConditionalException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        self.error_message = error_message


def handle_exception(e):
    if hasattr(e, 'response') :
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            error_message = 'Resource Not found'
            error_code = 404
    else:
        error_message = str(e)
        error_code = 500
    return jsonify({'status': 'error', 'message': error_message}), error_code
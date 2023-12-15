from flask import jsonify

class MissingResourceException(Exception):
    def __init__(self):
        super().__init__()
        self.error_message = 'Resource Not found'
        self.error_code  = 404


def handle_exception(e):
    if isinstance(e, MissingResourceException):
        error_message = 'Resource Not found'
        error_code = 404
    else:
        error_message = str(e)
        error_code = 500
    return jsonify({'status': 'error', 'message': error_message}), error_code
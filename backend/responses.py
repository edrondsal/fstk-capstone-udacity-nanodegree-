import os
from flask import jsonify

class AppError(Exception):
    def __init__(self, status_code, title, detail,type_error = None):
        self.status_code = status_code
        self.type_url = type_error if type_error is not None else "about:blank"
        self.title = title
        self.detail = detail

class Response(object):
    @staticmethod
    def success_response(responseStruct):
        response = {
            'success': True,
            'data': responseStruct
            }
        return jsonify(response)
    @staticmethod
    def error_response(app_error):
        response = {
            'success': False,
            'status': app_error.status_code,
            'type': app_error.type_url,
            'title': app_error.title,
            'detail': app_error.detail,
            'instance': "about:blank"
            }
        return jsonify(response)
import os
from flask import jsonify


class Response(object):
    @staticmethod
    def success_response(responseStruct):
        response = {
            'success': True,
            'data': responseStruct
            }
        return jsonify(response)
    @staticmethod
    def error_response(statusCode,title,detail,type_url=None):
        response = {
            'success': False,
            'status': statusCode,
            'type': type_url if type_url is not None else "about:blank",
            'title': title,
            'detail': detail,
            'instance': "about:blank"
            }
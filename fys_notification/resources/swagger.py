from flask_restful import Resource
from flask import send_file


class StaticResource(Resource):
    def get(self):
        return send_file('swagger.yml')

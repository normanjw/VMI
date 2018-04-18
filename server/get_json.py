from flask_restful import Resource
import logging
import json
from flask.json import jsonify
import os


class GetJson(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_relative_path(self):
        relative_path = ""
        if os.getcwd() == '/':
            relative_path = '/home/pi/Desktop/raspberry_pi/scale/drawer_status.json'
        else:
            relative_path = '/Users/jaz/Desktop/VMI/scale/drawer_status.json'
        return relative_path

    def get(self):
        print("Get request made:")
        print("Retrieving local sensor data:")
        relative_path = self.get_relative_path()
        with open(relative_path) as json_data:
            drawer = json.load(json_data)
            json_data.close()

        print('Content from local filesystem: {}'.format(drawer))
        return jsonify(drawer)


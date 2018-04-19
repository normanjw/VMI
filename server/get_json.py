from flask_restful import Resource
import logging
import json
from flask.json import jsonify


class GetJson(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scale_dirpath = '/home/pi/Desktop/VMI/scale/'

    def get(self):
        print("Get request made:")
        print("Retrieving local sensor data:")
        path = self.scale_dirpath + 'drawer_status.json'
        with open(path) as json_data:
            drawer = json.load(json_data)
            json_data.close()

        print('Content from local filesystem: {}'.format(drawer))
        return jsonify(drawer)


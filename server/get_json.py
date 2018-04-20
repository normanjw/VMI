import json
import logging
from flask.json import jsonify
from flask_restful import Resource
import env_vars


class GetJson(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_file = 'drawer_status.json'

    def get(self):
        print("Get request made:")
        print("Retrieving local sensor data:")
        path = env_vars.base_path + 'scale/' + self.data_file
        with open(path) as json_data:
            drawer = json.load(json_data)
            json_data.close()

        print('Content from local filesystem: {}'.format(drawer))
        return jsonify(drawer)


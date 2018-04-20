import logging

import flask
import flask_cors
import flask_restful
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from Settings import env_vars
from server.get_json import GetJson

app = flask.Flask(__name__)
api = flask_restful.Api(app)
cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": "*"}})
logger = logging.getLogger(__name__)
api.add_resource(GetJson, '/api/v1/VMI/get_sensor_data')


if __name__ == '__main__':
    logger.info("server starting on port " + str(env_vars.port_num) + ":")
    print('server starting on port ' + str(env_vars.port_num))
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port=env_vars.port_num)
    IOLoop.instance().start()

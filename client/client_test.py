import requests
from Configs import env_vars


def client_test():
    """
    tests server/client connection
    :return: http response code
    """
    url = 'http://' + env_vars.host + ':' + str(env_vars.port_num) + '/api/v1/VMI/get_sensor_data'
    print('Retrieving data from: "http://' + env_vars.host + ':' + str(env_vars.port_num)
          + '/api/v1/VMI/get_sensor_data"')
    response = requests.get(url)
    print("Status Code:" + str(response.status_code))
    print(f'Content from ' + env_vars.host + ':' + str(env_vars.port_num) + ': {response.content}')


client_test()


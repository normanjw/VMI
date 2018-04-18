import requests
import os


def get_host():
    host = ""
    if os.getcwd() == '/':
        host = '192.168.43.87'
    else:
        host = 'localhost'
    return host


def client_test():
    """
    tests server/client connection
    :return: http response code
    """
    host = get_host()
    url = 'http://' + host + ':3003/api/v1/VMI/get_sensor_data'
    print('Retrieving data from: "http://' + host + ':3003/api/v1/VMI/get_sensor_data"')
    response = requests.get(url)
    print("Status Code:" + str(response.status_code))
    print(f'Content from localhost:3003: {response.content}')


client_test()


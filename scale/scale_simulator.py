import random
import datetime
import json
import os
import time


def set_database_path():
    database_path = ""
    if os.getcwd() == '/':
        database_path = '/home/pi/Desktop/VMI/scale/drawer_database.json'
    else:
        database_path = 'drawer_database.json'
    return database_path

def get_drawer_data():
    """
    pull the data for the drawer
    :return:
    drawer data in JSON format
    contains: drawer number, weight per item in kg, item type
    """
    database_path = set_database_path()
    with open(database_path) as json_data:
        drawer_data = json.load(json_data)
        json_data.close()
        return drawer_data


def get_weight():
    """
    generates random weight between 0 and 1kg
    :return:
    weight in kg
    """
    return random.uniform(0, 2)


def get_num_items(data):
    """
    calculates number of items in drawer
    :param data: json with data for drawer
    :return: number of items per drawer rounded up to nearest integer
    """
    weight = get_weight()
    kg_per_item = float(data['kg_per_item'])
    return int(weight / kg_per_item)


def get_datetime():
    raw_datetime = str(datetime.datetime.now())
    status_date_str = raw_datetime.split(".")[0]
    date = status_date_str.split(" ")[0]
    time = status_date_str.split(" ")[1]
    date_time = str(date + "T" + time)
    return date_time


# def get_datetime():
#     return str(datetime.datetime.now())

def refresh_drawer_status():
    """

    :return:
    """
    drawer_data = get_drawer_data()
    drawer_status = {
        "item_type": drawer_data['item_type'],
        "quantity": get_num_items(drawer_data),
        "drawer_number": drawer_data['drawer_number'],
        "date_time": get_datetime()
    }
    return drawer_status


def write_to_file(drawer_status):
    with open('drawer_status.json', 'w') as outfile:
        json.dump(drawer_status, outfile)
        print(drawer_status)


def run():
    write_to_file(refresh_drawer_status())


while True:
    run()
    time.sleep(5)

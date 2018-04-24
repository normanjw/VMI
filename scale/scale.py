import datetime
import json
from hx711 import HX711
import math
base_path = '/home/pi/Desktop/VMI/'


def get_drawer_database():
    """
    pull the data for the drawer
    :return:
    drawer data in JSON format
    contains: drawer number, weight per item in kg, item type
    """
    with open(base_path + 'scale/' + 'drawer_database.json') as json_data:
        drawer_database = json.load(json_data)
        json_data.close()
        return drawer_database


def get_num_items(drawer_database):
    """
    gets number of items based on kg per item in drawer
    :param drawer_database: static drawer data in json format
    :return:
    """
    weight = get_weight()
    kg_per_item = float(drawer_database['kg_per_item'])
    float_num_items = float(weight/kg_per_item)
    difference = math.ceil(float_num_items) - float_num_items
    if difference < 0.5:
        num_items = math.floor(float_num_items)
    else:
        num_items = math.ceil(float_num_items)
    return num_items


def get_datetime():
    raw_datetime = str(datetime.datetime.now())
    status_date_str = raw_datetime.split(".")[0]
    date = status_date_str.split(" ")[0]
    time_24hr = status_date_str.split(" ")[1]
    date_time = str(date + "T" + time_24hr)
    return date_time


def refresh_drawer_status():
    """
    :return: dynamic drawer status
    """
    drawer_database = get_drawer_database()
    drawer_status = {
        "drawers": [{
            "drawer_num": drawer_database['drawer_number'],
            "item_type": drawer_database['item_type'],
            "quantity": get_num_items(drawer_database)
        }]
    }
    return drawer_status


def write_to_file(drawer_status):
    """
    writes to file current inventory statuses
    :param drawer_status: json with inventory stats for one drawer
    :return: None
    """
    with open(base_path + 'scale/' + 'drawer_status.json', 'w') as outfile:
        json.dump(drawer_status, outfile)

def get_weight():
    """
    generates random weight between 0 and 1kg
    :return:
    weight in kg
    """
    weight = hx.read_weight_kg()
    hx.cycle()
    return weight


if __name__ == "__main__":
    hx = HX711(5, 6)
    hx.set_offset(8348927)
    hx.set_ratio(-1.001335398)

    while True:
        try:
            drawer_status = refresh_drawer_status()
            write_to_file(drawer_status)
        except(KeyboardInterrupt, SystemExit):
            hx.clean_and_exit()

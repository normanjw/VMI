import json
import random
import time
base_path = '/home/pi/Desktop/VMI/'


def get_num_drawers():
    database = get_data()
    return len(database['drawers'])


def get_data():
    with open(base_path + '/scale/drawer_status.json') as json_data:
        data = json.load(json_data)
        json_data.close()
        return data


def refresh_drawer_status():
    """

    :return: dynamic drawer status
    """
    drawer_status = get_data()
    for drawer_num in range(num_drawers):
        drawer_status['drawers'][drawer_num]['quantity'] = random.randint(0, 50)
    write_to_file(drawer_status)
    return drawer_status


def write_to_file(drawer_status):
    with open(base_path + '/scale/drawer_status.json', 'w') as outfile:
        json.dump(drawer_status, outfile)


if __name__ == '__main__':
    num_drawers = get_num_drawers()
    while True:
        refresh_drawer_status()
        time.sleep(5)

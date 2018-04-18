from guizero import *
import requests
import json
import os
import time


def get_host():
    host = ""
    if os.getcwd() == '/':
        host = '192.168.43.87'
    else:
        host = 'localhost'
    return host


def get_drawer_data():
    host = get_host()
    url = 'http://' + host + ':3003/api/v1/VMI/get_sensor_data'
    print('Retrieving data from: ' + 'http://' + host + ':3003/api/v1/VMI/get_sensor_data')
    response = requests.get(url)
    print("Status Code:" + str(response.status_code))
    print(f'Content from ' + host + ':3003: {response.content}')
    drawer_data = json.loads(response.content)
    return drawer_data


def get_num_items():
    drawer_data = get_drawer_data()
    return drawer_data['quantity']


def update_text():
    num_items = get_num_items()
    if int(num_items) != 0:
        text.value = num_items
    else:
        text.value = num_items
        response = yesno("Confirmation", "Is drawer 1 empty?")
        if response:
            info("Confirmation", "Response logged: Drawer 1 Empty")
        else:
            info("Confirmation", "Response logged: Drawer 1 NOT Empty")

    text.after(3000, update_text)


def get_item_type(drawer_data):
    return drawer_data['item_type']


def get_drawer_num(drawer_data):
    return drawer_data['drawer_number']


def get_date(drawer_data):
    date_time = drawer_data['date_time']
    date = date_time.split('T')[0]
    return date


def get_time(drawer_data):
    date_time = drawer_data['date_time']
    t = date_time.split('T')[1]
    time_24hour = t.split(':')[0] + ':' + t.split(':')[1]
    t = time.strptime(time_24hour, "%H:%M")
    time_12hour = time.strftime("%I:%M %p", t)
    return time_12hour


if __name__ == '__main__':
    inventory_data = get_drawer_data()
    print(inventory_data)
    status_window = App(title='Inventory Status', height=200, width=300, layout='grid')
    Text(status_window, 'Date:', size="24", grid=[0, 0])
    Text(status_window, get_date(inventory_data), size="24", grid=[1, 0])
    Text(status_window, 'Time:', size="24", grid=[0, 1])
    Text(status_window, get_time(inventory_data), size="24", grid=[1, 1])
    Text(status_window, 'Drawer:', size="24", grid=[0, 2])
    Text(status_window, str(get_drawer_num(inventory_data)), size="24", grid=[1, 2])
    Text(status_window, 'Item type:', size="24", grid=[0, 3])
    Text(status_window, get_item_type(inventory_data), size="24", grid=[1, 3])
    Text(status_window, 'Quantity:', size="24", grid=[0, 4])
    text = Text(status_window, "xx", size="24", grid=[1, 4])
    text.after(1000, update_text)
    status_window.display()

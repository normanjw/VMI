import json
import logging
import time
import requests
from guizero import *
from Configs import env_vars


class InventoryStatus:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.item_quantity = None

    def get_drawer_data(self):
        """
        makes get request for drawer status
        :return: json of drawer data
        """
        host = str(env_vars.host)
        port_num = str(env_vars.port_num)
        url = 'http://' + host + ':' + port_num + '/api/v1/VMI/get_sensor_data'
        print('Retrieving data from: ' + 'http://' + host + ':' + port_num + '/api/v1/VMI/get_sensor_data')
        response = requests.get(url)
        print("Status Code:" + str(response.status_code))
        print(f'Content from ' + host + ':' + port_num + ':' + '{response.content}')
        drawer_data = json.loads(response.content)
        return drawer_data

    def get_num_items(self):
        drawer_data = self.get_drawer_data()
        return drawer_data['quantity']

    def update_quantity(self):
        """
        updates item quantity value in GUI
        :return: None
        """
        num_items = self.get_num_items()
        if int(num_items) != 0:
            self.item_quantity.value = num_items
        else:
            self.item_quantity.value = num_items
            response = yesno("Confirmation", "Is drawer 1 empty?")
            if response:
                info("Confirmation", "Response logged: Drawer 1 Empty")
            else:
                info("Confirmation", "Response logged: Drawer 1 NOT Empty")
        self.item_quantity.after(3000, self.update_quantity)

    def get_item_type(self, drawer_data):
        return drawer_data['item_type']

    def get_drawer_num(self, drawer_data):
        return drawer_data['drawer_number']

    def get_date(self, drawer_data):
        """
        parse the date
        """
        date_time = drawer_data['date_time']
        date = date_time.split('T')[0]
        return date

    def get_time(self, drawer_data):
        """
        parse time and convert to 12 hours
        """
        date_time = drawer_data['date_time']
        t = date_time.split('T')[1]
        time_24hour = t.split(':')[0] + ':' + t.split(':')[1]
        t = time.strptime(time_24hour, "%H:%M")
        time_12hour = time.strftime("%I:%M %p", t)
        return time_12hour

    def create_window(self):
        """
        creates a simple visual display
        """
        status_window = App(title='Inventory Status', height=200, width=300, layout='grid')
        Text(status_window, 'Date:', size="24", grid=[0, 0])
        Text(status_window, self.get_date(inventory_data), size="24", grid=[1, 0])
        Text(status_window, 'Drawer:', size="24", grid=[0, 2])
        Text(status_window, str(self.get_drawer_num(inventory_data)), size="24", grid=[1, 2])
        Text(status_window, 'Item type:', size="24", grid=[0, 3])
        Text(status_window, self.get_item_type(inventory_data), size="24", grid=[1, 3])
        Text(status_window, 'Quantity:', size="24", grid=[0, 4])
        self.item_quantity = Text(status_window, "xx", size="24", grid=[1, 4])
        self.item_quantity.after(1000, self.update_quantity)
        status_window.display()


if __name__ == '__main__':
    inventory = InventoryStatus()
    inventory_data = inventory.get_drawer_data()
    inventory.create_window()

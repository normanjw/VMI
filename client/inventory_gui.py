import json
import logging
import random
from tkinter import *
import requests
import env_vars


class InventoryStatus:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.inventory_window = Tk()
        self.num_rows = 0
        self.num_cols = 3
        self.keys = ['drawer_num', 'item_type', 'quantity']
        self.num_drawers = self.get_num_drawers()

    def get_data(self):
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

    def get_num_drawers(self):
        database = self.get_data()
        return len(database['drawers'])

    def get_num_items(self):
        return random.randint(0, 10)

    def run_display(self):
        self.define_window()
        self.create_labels()
        self.set_values()
        self.inventory_window.mainloop()

    def define_window(self):
        self.inventory_window.configure(background="#222222")
        self.inventory_window.geometry('600x400')
        self.inventory_window.title("Inventory Status")

    def create_labels(self):
        self.num_rows += 1
        num_cols = 3
        row_num = 0
        titles = ['Drawer', 'Item', 'Quantity']
        for col_num in range(num_cols):
            lbl = Label(self.inventory_window, text=titles[col_num], fg="#0E80D5", font=("Helvetica", 24), width=10, anchor="w")
            lbl.grid(row=row_num, column=col_num)
            lbl.configure(background="#222222")

    def set_values(self):
        data = self.get_data()
        for row_num in range(len(data['drawers'])):
            self.num_rows += 1
            for col_num in range(self.num_cols):
                lbl = Label(self.inventory_window, text=data['drawers'][row_num][self.keys[col_num]], fg="#DDDDDD",
                            font=("Helvetica", 24), width=10, anchor="w")
                lbl.grid(row=row_num+1, column=col_num, sticky=W)
                lbl.configure(background="#222222")
                col_num += 1
        self.inventory_window.after(1000, inventory_status.set_values)


if __name__ == '__main__':
    inventory_status = InventoryStatus()
    inventory_status.run_display()


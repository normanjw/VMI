#!/usr/bin/env python
import os
import struct
from datetime import datetime
from time import sleep
import signal
import json
import math


class Scale:
    def __init__(self):
        self._currentWeight = 0
        self._environment = ''
        self.base_path = '/home/pi/Desktop/VMI/'
        self.out_path = self.base_path + 'scale/' + 'drawer_status.json'
        self.drawer_database = self.get_drawer_database()

    def get_drawer_database(self):
        """
        pull the data for the drawer
        :return:
        drawer data in JSON format
        contains: drawer number, weight per item in kg, item type
        """
        with open(self.base_path + 'scale/' + 'drawer_database.json') as json_data:
            drawer_database = json.load(json_data)
            json_data.close()
            return drawer_database

    def get_num_items(self):
        """
        gets number of items based on kg per item in drawer
        :return:
        """
        weight = self._currentWeight
        g_per_item = float(self.drawer_database['g_per_item'])
        num_items_as_float = round(weight / float(g_per_item), 3)
        difference = math.ceil(num_items_as_float) - num_items_as_float
        if difference < 0.5:
            num_items = math.ceil(num_items_as_float)
            return num_items
        else:
            num_items = math.floor(num_items_as_float)
            return num_items

    def update_inventory_status(self):
        """
        :return: dynamic drawer status
        """
        inventory_status = {"drawers": [
            {"drawer_num": self.drawer_database['drawer_number'], "item_type": self.drawer_database['item_type'],
             "quantity": self.get_num_items()},
            {"drawer_num": 2, "item_type": "Hex Nuts", "quantity": 19},
            {"drawer_num": 3, "item_type": "Hex Screws", "quantity": 15}
        ]}

        return inventory_status

    def write_JSON_to_file(self, output):
        """
        writes to file current inventory statuses
        :return: None
        """
        with open(self.out_path, 'w') as outfile:
            json.dump(output, outfile)

    def environment(self):
        if not self._environment:
            self._environment = os.environ.get("ENVIRONMENT")
            if not self._environment:
                self._environment = "prod"

        return self._environment

    def get_weight_in_grams(self, dev="/dev/usb/hiddev0"):
        """
        This device normally appears on /dev/usb/hiddev0, assume
        device still appears on this file handle.
        """
        # If we cannot find the USB device, return -1
        grams = -1
        try:
            with open(dev, 'r+b') as f:
                # Read 4 unsigned integers from USB device
                fmt = "IIII"
                bytes_to_read = struct.calcsize(fmt)
                r = f.read(bytes_to_read)
                usb_binary_read = struct.unpack(fmt, r)
                if len(usb_binary_read) == 4:
                    grams = usb_binary_read[3]
        except OSError:
            print("{0} - Failed to read from USB device".format(datetime.utcnow()))
        return grams

    def handle_alarm(self, signum, frame):
        raise Exception("signum: {0} - frame: {1}".format(signum, frame))

    def main(self):
        self._currentWeight = self.get_weight_in_grams()
        signal.signal(signal.SIGALRM, self.handle_alarm)

        while True:
            try:
                signal.alarm(5)
                self._currentWeight = self.get_weight_in_grams()
                print(self._currentWeight)
                inventory_status = self.update_inventory_status()
                self.write_JSON_to_file(inventory_status)
            finally:
                signal.alarm(0)
            sleep(1)


if __name__ == "__main__":
    scale = Scale()
    scale.main()

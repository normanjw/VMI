import datetime
import json
import logging
from hx711 import HX711
#import sys
#sys.path.append('/home/pi/Desktop/VMI/scale/')
#from Settings import env_vars


class Scale:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scale_dirpath = '/home/pi/Desktop/VMI/scale/'
        self.hx = HX711(5, 6)

    def get_drawer_database(self):
        """
        pull the data for the drawer
        :return:
        drawer data in JSON format
        contains: drawer number, weight per item in kg, item type
        """
        with open(self.scale_dirpath + 'drawer_database.json') as json_data:
            drawer_database = json.load(json_data)
            json_data.close()
            return drawer_database

    def get_num_items(self, drawer_database):
        """
        gets number of items based on kg per item in drawer
        :param drawer_database: static drawer data in json format
        :return:
        """
        weight = self.get_weight()
        kg_per_item = float(drawer_database['kg_per_item'])
        return int(weight / kg_per_item)

    def get_datetime(self):
        raw_datetime = str(datetime.datetime.now())
        status_date_str = raw_datetime.split(".")[0]
        date = status_date_str.split(" ")[0]
        time_24hr = status_date_str.split(" ")[1]
        date_time = str(date + "T" + time_24hr)
        return date_time

    def refresh_drawer_status(self):
        """
        :return: dynamic drawer status
        """
        drawer_database = self.get_drawer_database()
        drawer_status = {
            "item_type": drawer_database['item_type'],
            "quantity": self.get_num_items(drawer_database),
            "drawer_number": drawer_database['drawer_number'],
            "date_time": self.get_datetime()
        }
        return drawer_status

    def write_to_file(self, drawer_status):
        """
        writes to file current inventory statuses
        :param drawer_status: json with inventory stats for one drawer
        :return: None
        """
        with open(self.scale_dirpath + 'drawer_status.json', 'w') as outfile:
            json.dump(drawer_status, outfile)
            print(drawer_status)

    def get_weight(self):
        """
        generates random weight between 0 and 1kg
        :return:
        weight in kg
        """
        weight = self.hx.read_weight_kg()
        self.hx.cycle()
        return weight

    def calculate_offset(self):
        print("remove any weight from scale. hit enter when done.")
        input()
        offsets_measured = []
        for i in range(10):
            temp = self.hx.read_average()
            print(temp)
            offsets_measured.append(temp)
        o = sum(offsets_measured) / float(len(offsets_measured))
        self.hx.set_offset(o)

    def calculate_ratio(self):
        print("place then enter weight in grams: ")
        weight_actual = input()
        weights_measured = []
        for i in range(10):
            temp = self.hx.read_average()
            print(temp)
            weights_measured.append(temp)
        w = sum(weights_measured) / float(len(weights_measured))
        ratio = (float(w) - float(self.hx.get_offset())) / float(weight_actual)
        self.hx.set_scale(ratio)

    def calibrate(self):
        self.calculate_offset()
        self.calculate_ratio()


if __name__ == "__main__":
    scale = Scale()
    scale.calibrate()

    while True:
        try:
            drawer_status = scale.refresh_drawer_status()
            scale.write_to_file(drawer_status)
        except(KeyboardInterrupt, SystemExit):
            scale.hx.clean_and_exit()

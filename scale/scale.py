import datetime
import json
import logging
from hx711 import HX711
import sys
sys.path.append('/home/pi/Desktop/VMI/Settings/')
from Settings import env_vars


class Scale:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_drawer_database(self):
        """
        pull the data for the drawer
        :return:
        drawer data in JSON format
        contains: drawer number, weight per item in kg, item type
        """
        with open(env_vars.scale_dirpath + 'drawer_database.json') as json_data:
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
        with open(env_vars.scale_dirpath + 'drawer_status.json', 'w') as outfile:
            json.dump(drawer_status, outfile)
            print(drawer_status)

    def get_weight(self):
        """
        generates random weight between 0 and 1kg
        :return:
        weight in kg
        """
        weight = hx.read_weight_kg()
        hx.cycle()
        return weight


if __name__ == "__main__":
    scale = Scale()
    hx = HX711(5, 6)
    hx.set_offset(8441810.431)
    hx.set_scale(12.02637183)

    while True:
        try:
            drawer_status = scale.refresh_drawer_status()
            scale.write_to_file(drawer_status)
        except(KeyboardInterrupt, SystemExit):
            hx.clean_and_exit()

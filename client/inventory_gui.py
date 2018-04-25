import json
import logging
from tkinter import *
import requests
import env_vars
import math


class InventoryStatus:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.drawers_per_row = 4
        self.root = Tk()
        self.keys = ['drawer_num', 'item_type', 'quantity']
        self.num_drawers = self.get_num_drawers()
        self.num_rows = self.set_num_rows()
        self.main_width = self.set_main_window_width()
        self.main_height = self.set_main_window_height()
        self.main_window_canvas = None
        self.step = 220
        self.x_0 = 85
        self.y_0 = 300
        self.qty_text = []
        self.green = '#4fab5b'
        self.shadow_green = '#417b3e'
        self.red = '#df2b4f'
        self.shadow_red = '#a23838'
        self.yellow = '#fff68f'
        self.threshold = 0
        self.background_color = "#222222"
        self.message_color = '#999999'
        self.message_font = 'Informa Pro'
        self.icon_font = 'Helvetica'
        self.icon_font_size = 100
        self.box_outline_color = '#333333'
        self.box_fill_color = '#2A2A2A'
        self.outline_width = 1
        self.popup_window_size = '320x240'

    def set_main_window_width(self):
        """
        calculate main window width based on number of drawers in first row
        :return: width of main window
        """
        width = 410 * self.num_drawers - 200 * (self.num_drawers - 1)
        return width

    def set_num_rows(self):
        """
        determines number of rows in grid based on number of drawers
        :return: number of rows
        """
        if self.num_drawers % self.drawers_per_row:
            num_rows = math.ceil(self.num_drawers/self.drawers_per_row)\
                       + math.floor(self.num_drawers / self.drawers_per_row)
        else:
            num_rows = self.num_drawers/self.drawers_per_row
        return int(num_rows)

    def set_main_window_height(self):
        """
        determines height of main window based on number of rows
        :return: height of main window
        """
        height = 400 + (self.num_rows - 1) * 400
        return height

    def get_data(self):
        """
        makes GET request for drawer status
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
        """
        gets the number of drawers
        :return: number of drawers
        """
        database = self.get_data()
        return len(database['drawers'])

    def create_main_window_boxes(self):
        """
        creates larger boxes for main window
        :return: None
        """
        self.main_window_canvas = Canvas(self.root, width=1000, height=1000, highlightthickness=0)
        self.main_window_canvas.pack(side="left")
        self.main_window_canvas.configure(background=self.background_color)
        for i in range(self.num_drawers):
            x1 = self.x_0 + self.step * i
            y1 = self.x_0
            x2 = self.y_0 + self.step * i
            y2 = self.y_0
            coordinates = [x1, y1, x2, y2]
            self.create_canvas_box(self.main_window_canvas, coordinates)

    def get_quantities(self):
        """
        gets number of quantities per drawer
        :return: list of ints - quantities per drawer
        """
        quantities = []
        data = self.get_data()
        for i in range(len(data['drawers'])):
            qty = data['drawers'][i]['quantity']
            quantities.append(qty)
        return quantities

    def get_item_types(self):
        """
        gets the name of the item type per drawer
        :return: list of strings, item types
        """
        item_types = []
        data = self.get_data()
        for i in range(len(data['drawers'])):
            item_types.append(data['drawers'][i]['item_type'])
        return item_types

    def print_labels(self):
        """
        prints the labels for drawer number and item type for each box in the main window
        :return: None
        """
        item_types = self.get_item_types()
        for row in range(self.num_rows):
            for i in range(self.num_drawers - 3 * row):
                label_text = 'Drawer ' + str(i+1) + ': ' + item_types[i]
                self.main_window_canvas.create_text(self.x_0 + 70 + self.step * i, self.x_0 + 12 - (250 * row),
                                                    font=(self.message_font, 14),
                                                    text=label_text, fill=self.message_color)

    def build_window(self):
        """
        builds the main window
        :return: None
        """
        self.root.configure(background=self.background_color)
        self.root.geometry(str(self.main_width) + 'x' + str(self.main_height))
        self.root.title("Inventory Status")
        self.create_main_window_boxes()
        self.print_labels()
        self.set_quantities()

    def set_quantities(self):
        """
        displays the number of quantities per drawer in the main window
        :return: None
        """
        quantities = self.get_quantities()
        for i in range(self.num_drawers):
            text = self.main_window_canvas.create_text(self.x_0 + 110 + self.step * i, self.x_0 + 110,
                                                       font=(self.icon_font, self.icon_font_size),
                                                       text=quantities[i], fill='#4fab5b')
            self.qty_text.append(text)

    def update_quantities(self):
        """
        dynamically updates the display for quantities per drawer
        :return: None
        """
        quantities = self.get_quantities()
        for i in range(self.num_drawers):
            self.main_window_canvas.itemconfigure(self.qty_text[i], text=quantities[i])
            self.check_threshold()
            self.root.after(1000, self.update_quantities)

    def is_yellow(self, text_obj):
        """
        checks if text object is yellow
        :param text_obj: ID for a canvas text object
        :return: boolean for isYellow
        """
        color = self.main_window_canvas.itemcget(text_obj, 'fill')
        if color == self.yellow:
            return True
        else:
            return False

    def check_threshold(self):
        """
        checks if the number of items is below the threshold value
        if so, sets the color of the number of items
        below threshold = red, becomes clickable
        at or above above threshold = green
        :return: None
        """
        for i in range(len(self.qty_text)):
            if int(self.get_text_from_object(self.main_window_canvas, self.qty_text[i])) <= self.threshold\
                    and not (self.is_yellow(self.qty_text[i])):
                self.set_text_red(self.qty_text[i])
                self.activate_button(i, self.qty_text[i])
            elif int(self.get_text_from_object(self.main_window_canvas, self.qty_text[i])) > self.threshold:
                self.set_text_green(self.qty_text[i])

    def set_text_green(self, text_obj):
        """
        sets a canvas text object green
        :param text_obj: ID for canvas text object
        :return: None
        """
        self.main_window_canvas.itemconfigure(text_obj, fill=self.green, activefill=self.green)

    def set_text_red(self, text_obj):
        """
        sets a canvas text object red
        changes color when user hovers to indicate it is clickable
        :param text_obj: ID for canvas text object
        :return: None
        """
        self.main_window_canvas.itemconfigure(text_obj, fill=self.red, activefill=self.shadow_red)

    def set_text_yellow(self, text_obj):
        """
        sets a canvas text object yellow
        resets hover color to be static
        :param text_obj: ID for canvas text object
        :return: None
        """
        self.main_window_canvas.itemconfigure(text_obj, fill=self.yellow, activefill=self.yellow)
        self.deactivate_button(text_obj)

    def activate_button(self, drawer_num, text_obj):
        """
        makes the number of items clickable (activates button)
        :param drawer_num: int
        :param text_obj: ID for canvas text object
        :return: None
        """
        self.main_window_canvas.tag_bind(text_obj, '<ButtonRelease-1>', lambda x: [self.open_quantity_confirmation(
            drawer_num, text_obj)])

    def deactivate_button(self, text_obj):
        """
        makes the number of items unclickable (deactivates button)
        :param text_obj: ID for canvas text object
        :return: None
        """
        self.main_window_canvas.tag_unbind(text_obj, '<ButtonRelease-1>')

    def get_text_from_object(self, canvas, text_obj):
        """
        gets the text object from the main window canvas
        :param text_obj: quantity
        :param canvas: canvas object
        :return: string of text
        """
        text = canvas.itemcget(text_obj, 'text')
        return str(text)

    def open_quantity_confirmation(self, drawer_num, text_obj):
        """
        creates quantity confirmation window
        :param drawer_num: int
        :param text_obj: ID for canvas text object
        :return: None
        """
        qty_confirm_window = Toplevel(self.root)
        qty_confirm_window.title('Confirmation Portal')
        qty_confirm_window.geometry(self.popup_window_size)
        qty_confirm_window.configure(background=self.background_color)
        self.create_confirm_qty_msg(qty_confirm_window, drawer_num, text_obj)
        yes_no_canvas = Canvas(qty_confirm_window)
        self.add_yes_no_buttons(yes_no_canvas, qty_confirm_window, text_obj, is_quantity_window=True)
        qty_confirm_window.mainloop()

    def add_yes_no_buttons(self, canvas, window, text_obj, is_quantity_window):
        """
        creates yes/no buttons for popup windows
        :param canvas: Canvas object
        :param window: window object
        :param text_obj: ID for canvas text object
        :param is_quantity_window: Boolean to check which type of popup window it is (determines behavior on clicks)
        :return: None
        """
        canvas.configure(background=self.background_color, highlightthickness=0)
        yes_coordinates = [25, 0, 130, 105]
        no_coordinates = [150, 0, 255, 105]
        self.create_canvas_box(canvas, yes_coordinates)
        self.create_canvas_box(canvas, no_coordinates)
        self.create_yes_label(canvas, text_obj, window)
        self.create_no_label(canvas, text_obj, window, is_quantity_window)
        canvas.pack()

    def create_canvas_box(self, canvas, coordinates):
        """
        creates boxes in the window based on coordinates and color settings
        :param canvas: Canvas object
        :param coordinates: coordinates to place the box in the Canvas object
        :return: None
        """
        canvas.create_rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3],
                                width=self.outline_width, outline=self.box_outline_color, fill=self.box_fill_color)

    def create_yes_label(self, canvas, text_obj, current_window):
        """
        creates no button in popup window
        :param canvas: Canvas object
        :param text_obj: ID for canvas text object
        :param current_window: window object for current popup window
        :return: None
        """
        yes_label = canvas.create_text(75, 50, font=(self.icon_font, 50), text='Yes', fill=self.green,
                                       activefill=self.shadow_green)
        canvas.tag_bind(yes_label, '<ButtonRelease-1>',
                        lambda x: [self.set_text_yellow(text_obj), self.exit_window(current_window)])

    def create_no_label(self, canvas, text_obj, current_window, is_quantity_window):
        """
        creates no button in popup window
        :param canvas: Canvas object
        :param text_obj: ID for canvas text object
        :param current_window: window object for current popup window
        :param is_quantity_window: Boolean to check which type of popup window it is
        :return:
        """
        no_label = canvas.create_text(204, 50, font=(self.icon_font, 50), text='No', fill=self.red,
                                      activefill=self.shadow_red)
        if is_quantity_window:
            canvas.tag_bind(no_label, '<ButtonRelease-1>', lambda x: [self.exit_window(current_window),
                                                                      self.create_error_confirm_window(text_obj)])
        else:
            canvas.tag_bind(no_label, '<ButtonRelease-1>', lambda x: [self.exit_window(current_window)])

    def create_confirm_qty_msg(self, window, drawer_num, text_obj):
        """
        message to ask user to confirm quantity of items
        :param window: window object for current window to write to
        :param drawer_num: current drawer number
        :param text_obj: ID for canvas text object
        :return: None
        """
        item_types = self.get_item_types()
        message = 'Does Drawer ' + str(drawer_num) + ' contain '\
                  + self.get_text_from_object(self.main_window_canvas, text_obj) + ' ' + item_types[drawer_num] + '?'
        lbl = Label(window, text=message, bg=self.background_color, fg=self.message_color, font=(self.message_font, 20))
        lbl.pack(pady=30)

    def create_error_confirm_window(self, text_obj):
        """
        creates error confirmation popup window
        :param text_obj: ID for canvas text object
        :return: None
        """
        error_confirm_window = Toplevel(self.root)
        error_confirm_window.title('Error Confirmation Portal')
        error_confirm_window.geometry(self.popup_window_size)
        error_confirm_window.configure(background=self.background_color)
        error_confirm_canvas = Canvas(error_confirm_window)
        self.create_error_confirm_msg(error_confirm_window)
        self.add_yes_no_buttons(error_confirm_canvas, error_confirm_window, text_obj, is_quantity_window=False)
        error_confirm_canvas.pack()

    def create_error_confirm_msg(self, error_confirm_window):
        """
        creates error confirmation message in window
        :param error_confirm_window: error confirmation window object
        :return: None
        """
        Label(error_confirm_window, text='Confirm and log system error?', bg=self.background_color,
              font=(self.message_font, 20), fg=self.message_color).pack(pady=30)

    @staticmethod
    def exit_window(window):
        """
        destroys current window object
        :param window: current window object
        :return: None
        """
        window.destroy()

    def refresh_window(self):
        """
        refreshes the window
        :return: None
        """
        self.build_window()
        self.update_quantities()


if __name__ == '__main__':
    inventory_status = InventoryStatus()
    inventory_status.refresh_window()
    mainloop()

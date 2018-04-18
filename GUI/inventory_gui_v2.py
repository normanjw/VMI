from tkinter import *
import logging


class InventoryStatus:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.window = Tk()

    def run_display(self):
        self.define_window()
        self.create_labels()
        self.set_values()
        self.window.mainloop()

    def define_window(self):
        self.window.configure(background="#222222")
        self.window.geometry('600x400')
        self.window.title("Inventory Status")

    def create_labels(self):
        num_cols = 3
        row_num = 0
        titles = ['Drawer', 'Item', 'Quantity']
        for col_num in range(num_cols):
            lbl = Label(self.window, text=titles[col_num], fg="#0E80D5", font=("Helvetica", 24), width=10, anchor="w")
            lbl.grid(row=row_num, column=col_num)
            lbl.configure(background="#222222")

    def set_values(self):
        num_cols = 3
        values = [[1, 'screws', 87, 20], [2, 'bolts', 45, 10], [3, 'nuts', 12, 15]]
        for row_num in range(len(values)):
            row_num += 1
            for col_num in range(num_cols):
                lbl = Label(self.window, text=values[row_num-1][col_num], fg="#DDDDDD", font=("Helvetica", 24), width=10, anchor="w")
                lbl.grid(row=row_num, column=col_num, sticky=W)
                lbl.configure(background="#222222")
                col_num += 1
            threshold = values[row_num-1][col_num]
            quantity = values[row_num-1][col_num-1]
            if quantity <= threshold:
                print("confirm if low")


if __name__ == '__main__':
    inventory_status = InventoryStatus()
    inventory_status.run_display()

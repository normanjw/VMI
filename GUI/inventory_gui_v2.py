import smtplib
import base64
from tkinter import *
from tkinter import scrolledtext
import tkinter.messagebox

#mail = smtplib.SMTP('smtp.gmail.com',587)
#mail.ehlo()
#mail.starttls()
#mail.login('ece404vmi@gmail.com','vmiece404')
#mail.sendmail('ece404vmi@gmail.com','shind2@vcu.edu', 'Threshold reached. Ordering inventory.')
#mail.close()

#class

#class


# functions
def doSomething(self, master):
      print("Add functionality here..")
#creating window object

window = Tk()
w = Label(window, text="ECE 404: VMI")
w.grid(row=20,column=0)
window.configure(background="#EEEEEE")
tkinter.messagebox.showinfo('Welcome!', 'Welcome!!')
message = tkinter.messagebox.askquestion('Message','Show status of VMI system?')
if message == 'yes':
    print('Here are the current statuses.')

#txt = scrolledtext.ScrolledText(window, width=40, height=10)
#txt.grid(row=0,column=20)
#exit button
exitButton = Button(window, text="Click to Exit",command=window.destroy)
exitButton.grid(row=20,column=25)
#Menu
menu = Menu(window)
window.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Search...", command=doSomething)
subMenu.add_command(label="New...", command=doSomething)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=window.destroy)

editMenu = Menu(menu)
menu.add_cascade(label="Edit", command=editMenu)
editMenu.add_command(label="Redo...", command=doSomething)
#define labels
window.title("ECE 404 GUI")
    #bin 1
lbl0 = Label(window, text="Bin #1", font=("Helvetica Bold", 12, "italic"))
lbl0.grid(row=0, column=0)
lbl1 = Label(window, text="Product Name", font=("Arial Bold", 8))
lbl1.grid(row=1, column=1, sticky=W)
lbl2 = Label(window, text="Quantity", font=("Arial Bold", 8))
lbl2.grid(row=1, column=3, sticky=W)
lbl3 = Label(window, text="Warehouse Location", font=("Arial Bold", 8))
lbl3.grid(row=1, column=5, sticky=W)
lbl4 = Label(window, text="Availability", font=("Arial Bold", 8))
lbl4.grid(row=1, column=7, sticky=W)
lbl5 = Label(window, text="Reorder?", font=("Arial", 8))
lbl5.grid(row=1, column=17, sticky=E)
lbl6 = Label(window, text="How would you like to be notified?", font=("Arial", 9))
lbl6.grid(row=13, column=19)
    #bin 2
bintwo0 = Label(window, text="Bin #2", font=("Helvetica Bold", 12, "italic"))
bintwo0.grid(row=4, column=0)
bintwo1 = Label(window, text="Product Name", font=("Arial Bold", 8))
bintwo1.grid(row=5, column=1, sticky=W)
bintwo2 = Label(window, text="Quantity", font=("Arial Bold", 8))
bintwo2.grid(row=5, column=3, sticky=W)
bintwo3 = Label(window, text="Warehouse Location", font=("Arial Bold", 8))
bintwo3.grid(row=5, column=5, sticky=W)
bintwo4 = Label(window, text="Availability", font=("Arial Bold", 8))
bintwo4.grid(row=5, column=7, sticky=W)
bintwo5 = Label(window, text="Reorder?", font=("Arial", 8))
bintwo5.grid(row=5, column=17, sticky=E)
   #bin 3
binthree0 = Label(window, text="Bin #3", font=("Helvetica Bold", 12, "italic"))
binthree0.grid(row=7, column=0)
binthree1 = Label(window, text="Product Name", font=("Arial Bold", 8))
binthree1.grid(row=8, column=1, sticky=W)
binthree2 = Label(window, text="Quantity", font=("Arial Bold", 8))
binthree2.grid(row=8, column=3, sticky=W)
binthree3 = Label(window, text="Warehouse Location", font=("Arial Bold", 8))
binthree3.grid(row=8, column=5, sticky=W)
binthree4 = Label(window, text="Availability", font=("Arial Bold", 8))
binthree4.grid(row=8, column=7, sticky=W)
binthree5 = Label(window, text="Reorder?", font=("Arial", 8))
binthree5.grid(row=8, column=17, sticky=E)
#lbl6 = Label(window, text="Mark if Yes", font=("Arial", 6, "italic"))
#lbl6.grid(column=20, row=1)
window.geometry('1000x425')
#define entries
   #bin 1
product_text=StringVar()
b1e1=Entry(window,textvariable=product_text)
b1e1.grid(row=2, column=1)
quantity_text=StringVar()
b1e2=Entry(window,textvariable=quantity_text)
b1e2.grid(row=2, column=3)
warehouse_text=StringVar()
b1e3=Entry(window,textvariable=warehouse_text)
b1e3.grid(row=2, column=5)
availability_text=StringVar()
b1e4=Entry(window,textvariable=availability_text)
b1e4.grid(row=2, column=7)
   #bin 2
product1_text=StringVar()
b2e1=Entry(window,textvariable=product1_text)
b2e1.grid(row=6, column=1)
quantity1_text=StringVar()
b2e2=Entry(window,textvariable=quantity1_text)
b2e2.grid(row=6, column=3)
warehouse1_text=StringVar()
b2e3=Entry(window,textvariable=warehouse1_text)
b2e3.grid(row=6, column=5)
availability1_text=StringVar()
b2e4=Entry(window,textvariable=availability1_text)
b2e4.grid(row=6, column=7)
    #bin 3
product2_text=StringVar()
b3e1=Entry(window,textvariable=product2_text)
b3e1.grid(row=9, column=1)
quantity2_text=StringVar()
b3e2=Entry(window,textvariable=quantity2_text)
b3e2.grid(row=9, column=3)
warehouse2_text=StringVar()
b3e3=Entry(window,textvariable=warehouse2_text)
b3e3.grid(row=9, column=5)
availability2_text=StringVar()
b3e4=Entry(window,textvariable=availability2_text)
b3e4.grid(row=9, column=7)
#radiobutton (check if reship)
r1=Radiobutton(window, text="Mark if Yes",padx=40,value=1)
r1.grid(row=2, column=17)
r2=Radiobutton(window, text="Mark if Yes",padx=40,value=2)
r2.grid(row=6, column=17)
r3=Radiobutton(window, text="Mark if Yes",padx=40,value=3)
r3.grid(row=9, column=17)

#listbox (notify by)
list1=Listbox(window)
list1.insert(1,'SMS')
list1.insert(2,'E-Mail')
list1.insert(3,'Both')
list1.grid(row=12, column=19)

#class newWindow:
#
 #   def __init__(self, master):
  #      frame = Frame(master)
   #     frame.pack()
#
#        self.printButton = Button(frame, text = "test message", command=self.printMessage)
 #       self.printButton.pack(side=LEFT)
#
 #       self.quitButton = Button(frame, text="Quit",command=frame.quit)
  #      self.quitButton.pack(side=LEFT)

   # def printMessage(self):
   #     print("Test, is it working?")
#
#def clicked():
#    lbl.configure(text="Button has been clicked")
#btn = Button(window, text="Test Button", command=clicked)
#btn.grid(row=1, column=0)

window.mainloop()
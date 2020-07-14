import Tkinter as tk
from Tkinter import tkk
import tkFont
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class edit_data_page(object):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = tk.title(self, "Edit Values Page")

        text = tk.Label(text="Edit Data Page", font=("Times New Roman",14)))
        text.pack()
        heading= tkFont.Font(text, text.cget("font"))
        text.configure(underline = True)
        heading.configure(font=text)

        #save button
        ##edited info here will be written on the csv, then the button just goes back to the graphing_page
        #to be updated
        save_button = tkk.Button(self, text="Save changes", command = lambda: controller.show_frame(graphing_page))

        #discard button
        discard_button = tkk.Button(self, text="Discard", command = lambda: controller.show_frame(graphing_page))
        discard_button.pack()

        #go and edit the csv yourself because you are adding another axis to the plot
        open_csv_button = tkk.Button(self, text="Edit File", command = lambda: controller.open_csv())
        open_csv_button.pack()
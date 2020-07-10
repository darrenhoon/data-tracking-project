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
        self.title = tk.title(self, "Plot Page")
        controller.frames[self]= self(controller.container, controller)
        self.grid(row=0,column=0,sticky="nsew")

        text = tk.Label(text="Edit Data Page", font=("Arial",12)))
        text.pack()
        heading= tkFont.Font(text, text.cget("font"))
        text.configure(underline = True)
        heading.configure(font=text)

        #save button

        #discard button

        #go and edit the csv yourself because you are adding another axis to the plot
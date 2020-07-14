import tkinter as tk
from tkinter import ttk
from tkinter import font
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

#controller is the datatrackerapp, parent is the main_menu

class graphing_page:
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = tk.title(self, "Plot Page")

        ##this part can be edited if we do not want underline for the whole heading
        text = tk.Label(text="Plotting Page", font=("Arial",12))
        text.pack()
        heading= font.Font(text, text.cget("font"))
        text.configure(underline = True)
        heading.configure(font=text)

        # if the above underlining causes issues, use the below code which has no underline
        # label = tk.label(self, text="Plotting Page", font=("Arial",12))
        # label.pack(pady=500,padx=500)

        controller.add_frame(self)

        #back to main menu button
        back_button = ttk.Button(self, text="Back to Main Menu", command = lambda: controller.show_frame(parent))
        back_button.pack()

        #to add a new button that opens the edit data page. edit_data_page is the class name for the edit data page
        edit_data_page_button = ttk.Button(self, text="Edit Data", command = lambda: controller.show_frame(edit_data_page))
        edit_data_page_button.pack()

        

        #plot the graph on matplotlib's side first
        fig = Figure(figsize(5,5), dpi=100)

        # to show the plotted graph above on the window of tkinter. INSERT DATA EXTRACTED FROM CSV HERE. #need to do: once data is passed here,
        # need to evaluate if the data is 2d or 3d graph
        #@ BoonJuey pls edit this data = controller.list() to fit your datatype

        data = controller.list()
        graph=fig.add_subsplot(111)
        if len(data)>3:
            raise Exception("You cannot plot graphs with more than 3 dimensions! Go do math mods instead!")
        elif len(data)==3:
            graph=fig.add_subsplot(111, projection="3d")

        page = FigureCanvasTkAgg(fig,master=controller)
        page.draw()
        page.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        #toolbar page, for futher applications to edit saved data
        toolbar=NavigationToolbar2Tk(page,self)
        toolbar.update()
        page.tkcanvas.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

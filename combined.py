import tkinter as tk
from tkinter import ttk
from tkinter import font
import matplotlib
matplotlib.use("TkAgg")
from tkinter.ttk import *
from subprocess import Popen
from tkinter import filedialog
import os
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class Datatrackingapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side='top',fill='both',expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage,graphing_page,edit_data_page): #to be edited upon adding pagetwo
            self.add_frame(f)
            # frame = f(container,self) 
            # self.frames[f] = frame
            # frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()

    def add_frame(self,f):
        frame = f(self.container,self)
        self.frames[f]=frame
        frame.grid(row=0,column=0,sticky="nsew")
    
    def open_csv(self):

        tkinter.messagebox.showinfo("Warning","The program will now shut down and the data spreadsheet will be opened. Please wait a few moment for your pc to open \
            the excel/csv file. Thank you!")

        #approach 1: use pop open
        #p = Popen('filename.csv', shell=True)
        #exit_button = tk.Button(self, text='Exit',command = quit)
        #if above does not work, use this below but the filepath must be specific to where your MS Excel is stored in your pc.
        # subprocess.Popen(r'C:\Program Files (x86)\Microsoft Office\Office14\EXCEL.EXE stack.csv')

        #approach 2: use os to open filename
        filename = filedialog.askopenfilename(initialdir="C:/", title="select file")
        os.system(filename)
        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Data Tracker 2020", font="Helvetica 16 bold italic",justify=tk.CENTER,
        fg='white',bg='black')
        label.grid(row=0,column=2)

        style = Style()
        style.configure('TButton', font=('Arial',10,'bold'), foreground = 'red',
        background = 'black')
        style.map('TButton', background = [('active','black')], 
        foreground = [('active', 'navy')])

        plot_button = Button(self, text='Start Plot!', command = lambda: controller.show_frame(graphing_page))
        plot_button.grid(row=1,column=2)

        exit_button = Button(self, text='Exit',command = quit)
        exit_button.grid(row=2,column=2)

class graphing_page:
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = tk.title(self, "Plot Page")

        ##this part can be edited if we do not want underline for the whole heading
        #text = tk.Label(text="Plotting Page", font=("Arial",12))
        #text.pack()
        #heading= font.Font(text, text.cget("font"))
        #text.configure(underline = True)
        #heading.configure(font=text)

        # if the above underlining causes issues, use the below code which has no underline
        label = tk.label(self, text="Plotting Page", font=("Arial",12))
        label.pack(pady=500,padx=500)

        #back to main menu button
        back_button = ttk.Button(self, text="Back to Main Menu", command = lambda: controller.show_frame(StartPage))
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

class edit_data_page(object):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = tk.title(self, "Edit Values Page")

        text = tk.Label(text="Edit Data Page", font=("Times New Roman",14))
        text.pack()
        heading= font.Font(text, text.cget("font"))
        text.configure(underline = True)
        heading.configure(font=text)

        #save button
        ##edited info here will be written on the csv, then the button just goes back to the graphing_page
        #to be updated
        save_button = ttk.Button(self, text="Save changes", command = lambda: controller.show_frame(graphing_page))

        #discard button
        discard_button = ttk.Button(self, text="Discard", command = lambda: controller.show_frame(graphing_page))
        discard_button.pack()

        #go and edit the csv yourself because you are adding another axis to the plot
        open_csv_button = ttk.Button(self, text="Edit File", command = lambda: controller.open_csv())
        open_csv_button.pack()


if __name__ == "__main__":
    app = Datatrackingapp()
    app.title('Data Tracker')
    
    # app.geometry('400x400')
    app.mainloop()


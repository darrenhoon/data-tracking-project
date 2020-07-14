import tkinter as tk
from tkinter import ttk, font, filedialog
import matplotlib
matplotlib.use("TkAgg")
from tkinter.ttk import *
import subprocess, os, platform
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class Datatrackingapp(tk.Tk): #root window

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side='top',fill='both',expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage,graphing_page,edit_data_page):
            # self.add_frame(f)
            frame = f(self.container,self) 
            self.frames[f] = frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()

    def add_frame(self,f):
        frame = f(self.container,self)
        self.frames[f]=frame
        frame.grid(row=0,column=0,sticky="nsew")
    
    def open_csv(self):

        tkinter.messagebox.showinfo("Warning","The program will now shut down and the data spreadsheet will be opened. Please wait a few moment\
for your pc to open your selected file. Thank you!")
        
        filepath = filedialog.askopenfilename(initialdir="C:/", title="select file")
        print(filepath)
        #big creds to https://stackoverflow.com/questions/434597/open-document-with-default-os-application-in-python-both-in-windows-and-mac-os
        # ily :')
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
        quit()
        

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.controller.title("Data Tracker")
        
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

class graphing_page(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.controller.title("Plot Page")

        label = tk.Label(self, text="Plotting Page", font=("Arial",12))
        #label.pack(pady=500,padx=500)

        back_button = ttk.Button(self, text="Back to Main Menu", command = lambda: controller.show_frame(StartPage))
        back_button.pack()

        edit_data_page_button = ttk.Button(self, text="Edit Data", command = lambda: controller.show_frame(edit_data_page))
        edit_data_page_button.pack()

        fig = Figure(figsize=(5,5), dpi=100)

        data = [[0,1,2,3,4,5,6],[7,6,5,4,3,2,1]] ##data to be edited
        graph=fig.add_subplot(111)
        if len(data)>3:
            raise Exception("You cannot plot graphs with more than 3 dimensions! Go do math mods instead!")
        elif len(data)==3:
            graph=fig.add_subplot(111, projection="3d")

        graph.plot(data)
        page = FigureCanvasTkAgg(fig,master=controller)
        page.draw()
        

class edit_data_page(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.controller.title("Edit Values Page")

        text = tk.Label(text="Edit Data Page", font=("Times New Roman",14))
        text.pack()
        heading= font.Font(text, text.cget("font"))
        text.configure(underline = True)

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
    # app.geometry('400x400')
    app.mainloop()


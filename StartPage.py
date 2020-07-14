import tkinter as tk
from tkinter.ttk import *
from subprocess import Popen
from tkinter import filedialog
import os
import tkinter.messagebox

class Datatrackingapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side='top',fill='both',expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage,): #to be edited upon adding pagetwo
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
        # frame = self(controller.container,controller)
        # controller.frame[self]= frame
        # frame.grid(row=0,column=0,sticky='nsew')
        
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

if __name__ == "__main__":
    app = Datatrackingapp()
    app.title('Data Tracker')
    
    # app.geometry('400x400')
    app.mainloop()
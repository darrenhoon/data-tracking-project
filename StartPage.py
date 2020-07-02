import tkinter as tk
from tkinter.ttk import *

class Datatrackingapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top',fill='both',expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage,): #to be edited upon adding pagetwo
            frame = f(container,self)
            self.frames[f] = frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()

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

        plot_button = Button(self, text='Start Plot!', command = lambda: func('Next Page'))
        plot_button.grid(row=1,column=2)

        exit_button = Button(self, text='Exit',command = quit)
        exit_button.grid(row=2,column=2)

def func(text):
    print(text)

app = Datatrackingapp()
app.title('Data Tracker')
# app.geometry('400x400')
app.mainloop()
import tkinter as tk
from tkinter import ttk

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
        label = tk.Label(self, text="Data-Tracker 2020", font=('Arial',12))
        label.pack(pady=10,padx=10)

        exit_button = ttk.Button(self, text='Exit',
        command = quit)
        exit_button.pack()

        # plot_button = ttk.Button(self, text='Start Plot!', 
        # command = lambda: controller.show_frame(page_two))
        # plot_button.pack()

app = Datatrackingapp()
app.mainloop()
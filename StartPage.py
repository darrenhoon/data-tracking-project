import tkinter as tk

class Datatrackingapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side='top',fill='both',expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container,self)
        self.frames[StartPage] = frame
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

        exit_button = tk.Button(self, text='Exit',
        command = lambda: func('Hope you enjoyed using our app!'))
        exit_button.pack()

        plot_button = tk.Button(self, text='Start Plot!', 
        command = lambda: func('Next Page'))
        plot_button.pack()

def func(text):
    print(text)

app = Datatrackingapp()
app.mainloop()
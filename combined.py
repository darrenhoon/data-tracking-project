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

        tkinter.messagebox.showinfo("Warning","The program will now shut down and the data spreadsheet will be opened. Please wait a few moment \
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
        #label.grid(row=0,column=2)
        label.pack(side=tk.TOP,padx=10,pady=10)

        style = Style()
        style.configure('TButton', font=('Arial',10,'bold'), foreground = 'red',
        background = 'black')
        style.map('TButton', background = [('active','black')], 
        foreground = [('active', 'navy')])

        plot_button = Button(self, text='Start Plot!', command = lambda: controller.show_frame(graphing_page))
        #plot_button.grid(row=1,column=2)
        plot_button.pack(side=tk.TOP,padx=10,pady=10)

        exit_button = Button(self, text='Exit',command = quit)
        #exit_button.grid(row=2,column=2)
        exit_button.pack(side=tk.TOP,padx=10,pady=10)

class graphing_page(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.controller.title("Plot Page")

        label = tk.Label(self, text="Plotting Page", font=("Arial",12))
        #label.pack(pady=500,padx=500)

        edit_data_page_button = ttk.Button(self, text="Edit Data", command = lambda: controller.show_frame(edit_data_page))
        edit_data_page_button.pack(side=tk.TOP,padx=10,pady=10)

        back_button = ttk.Button(self, text="Back to Main Menu", command = lambda: controller.show_frame(StartPage))
        back_button.pack(side=tk.TOP,padx=10)

        fig = Figure(figsize=(5,5), dpi=100)
        graph=fig.add_subplot(111)
        data = [[0.5,1.2,2.8,3,4,6,7],[0,3,4,4.5,6,10,9]] ##data to be edited
        if len(data)>3:
            raise Exception("You cannot plot graphs with more than 3 dimensions! Go do math mods instead!")
        elif len(data)==3:
            graph=fig.add_subplot(111, projection="3d")

        graph.plot(data)
        #graph.ylabel("Sample y label")
        #graph.xlabel("Sample x label")
        #graph.axis([0,10,0,10]) #[xmin,xmax,ymin,ymax]
        # page = FigureCanvasTkAgg(fig,master=controller)
        page = FigureCanvasTkAgg(fig,self)
        page.draw()
        page.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)

class edit_data_page(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        self.controller.title("Edit Values Page")

        text = tk.Label(self,text="Edit Data Page", font=("Times New Roman",14))
        # text.pack()
        text.place(relx=0.5,anchor='n')
        heading= font.Font(text, text.cget("font"))
        # text.configure(underline = True) #Doesn't underline the entire text

        #save button
        ##edited info here will be written on the csv, then the button just goes back to the graphing_page
        #to be updated
        # save_button = ttk.Button(self, text="Save changes", command = lambda: controller.show_frame(graphing_page))
        save_button = ttk.Button(self, text="Save changes", command = lambda: controller.show_frame(graphing_page))
        # save_button.pack(padx=10,pady=10)
        save_button.place(relx=0.5,rely=0.1,anchor='n')

        #discard button
        discard_button = ttk.Button(self, text="Discard", command = lambda: controller.show_frame(graphing_page))
        # discard_button.pack(padx=10,pady=10)
        discard_button.place(relx=0.5,rely=0.15,anchor='n')

        #go and edit the csv yourself because you are adding another axis to the plot
        open_csv_button = ttk.Button(self, text="Edit File", command = lambda: controller.open_csv())
        # open_csv_button.pack(padx=10,pady=10)
        open_csv_button.place(relx=0.5,rely=0.2,anchor='n')

        #Display Data
        self.tree = Treeview(self, selectmode = 'none')
        # self.tree.pack(side='left',fill=tk.BOTH,expand=True)
        self.tree.place(rely=0.25,relx=0.15,relheight=0.5,relwidth=0.7)
        scrlbar = Scrollbar(self,orient='vertical',command=self.tree.yview)
        # scrlbar.pack(side='right',fill='y')
        scrlbar.place(rely=0.25,relx=0.96,relheight=0.5)
        self.tree.configure(yscrollcommand=scrlbar.set)

        #Tree components
        self.tree["columns"] = ("1", "2","3")
        self.tree['show'] = 'headings'
        self.tree.column("1", width=100, anchor='c')
        self.tree.column("2", width=100, anchor='c')
        self.tree.column("3", width=100, anchor='c')
        self.tree.heading("1", text="Index")
        self.tree.heading("2", text="Account")
        self.tree.heading("3", text="Type")
        self.tree.bind('<ButtonRelease-1>', self.select_item)

        #Sample data values
        self.tree.insert("",'end',text="L1",values=("1","Big1","Best"))
        self.tree.insert("",'end',text="L2",values=("2","Big2","Best"))
        self.tree.insert("",'end',text="L3",values=("3","Big3","Best"))
        self.tree.insert("",'end',text="L4",values=("4","Big4","Best"))
        self.tree.insert("",'end',text="L5",values=("5","Big5","Best"))
        self.tree.insert("",'end',text="L6",values=("6","Big6","Best"))
        self.tree.insert("",'end',text="L7",values=("7","Big7","Best"))
        self.tree.insert("",'end',text="L8",values=("8","Big8","Best"))
        self.tree.insert("",'end',text="L9",values=("9","Big9","Best"))
        self.tree.insert("",'end',text="L10",values=("10","Big10","Best"))
        self.tree.insert("",'end',text="L11",values=("11","Big11","Best"))
        self.tree.insert("",'end',text="L12",values=("12","Big12","Best"))
        self.tree.insert("",'end',text="L13",values=("13","Big13","Best"))
        self.tree.insert("",'end',text="L14",values=("14","Big14","Best"))
        self.tree.insert("",'end',text="L15",values=("15","Big15","Best"))
        self.tree.insert("",'end',text="L16",values=("16","Big16","Best"))

        #Entry to input values
        col1 = tk.Label(self,text='Column 1').place(rely=0.8,relx=0.07)
        col2 = tk.Label(self,text='Column 2').place(rely=0.8,relx=0.38)
        col3 = tk.Label(self,text='Column 3').place(rely=0.8,relx=0.69)

        col1_entry = tk.Entry(self).place(rely=0.85,relx=0.07)
        col2_entry = tk.Entry(self).place(rely=0.85,relx=0.38)
        col3_entry = tk.Entry(self).place(rely=0.85,relx=0.69)


    def select_item(self, event):
        curItem = self.tree.item(self.tree.focus())
        # curItem = self.tree.(self.tree.focus())
        col = self.tree.identify_column(event.x)
        print ('curItem = ', curItem)
        print ('col = ', col)

        if col == '#0':
            cell_value = curItem['text']
        elif col == '#1':
            cell_value = curItem['values'][0]
        elif col == '#2':
            cell_value = curItem['values'][1]
        elif col == '#3':
            cell_value = curItem['values'][2]

        print ('cell_value = ', cell_value)

if __name__ == "__main__":
    app = Datatrackingapp()
    # app.geometry('400x400')
    app.mainloop()
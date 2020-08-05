import tkinter as tk
from tkinter import ttk, font, filedialog
import matplotlib
matplotlib.use("TkAgg")
from tkinter.ttk import *
import subprocess, os, platform
import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import csv
import pandas as pd
import datetime
##global variables: variable1, variable2, variable3, data eg data[varialbe1]

class Datatrackingapp(tk.Tk): #root window

    def __init__(self, *args, **kwargs):
        
        #remember to import pandas
        csv_data = pd.read_csv('Spending.csv', header = None)
        global data
        global headers
        headers = csv_data.iloc[0]
        data = pd.DataFrame(csv_data.values[1:], columns=headers)
        #creates 2 different global variables for data and headers, both are pandas dataframe objects
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side='top',fill='both',expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (StartPage,edit_data_page):
            # self.add_frame(f)
            frame = f(self.container,self) 
            self.frames[f] = frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)
        
    def set_headers(self, var1, var2, var3):
        global variable1
        global variable2
        global variable3
        global plotting_data

        variable1 = str(var1.get())
        variable2 = str(var2.get())
        variable3 = str(var3.get())
        plotting_data = []
        
        plotting_vars = [variable1, variable2, variable3]
        for var in plotting_vars:
            if var == "-":
                continue
            elif var == "Date":
                values = [datetime.datetime.strptime(d,"%m/%d/%Y").date() for d in data[var].tolist()]
                plotting_data.append(values)
            else:
                values = data[var].tolist()
                values = [int(x) for x in values]
                print(values)
                plotting_data.append(values)

        frame = graphing_page(self.container,self)
        self.frames[graphing_page] = frame
        frame.grid(row=0,column=0,sticky="nsew")

        print(plotting_data)
        
        self.show_frame(graphing_page)
        

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

        optionHeads = list(headers)
        var1 = tk.StringVar()
        var1.set("-")
        option1 = tk.OptionMenu(self, var1, *optionHeads)
        option1.pack(side=tk.TOP,padx=10,pady=10)
        
        var2 = tk.StringVar()
        var2.set("-")
        option2 = tk.OptionMenu(self, var2, *optionHeads)
        option2.pack(side=tk.TOP,padx=10,pady=10)
        
        var3 = tk.StringVar()
        var3.set("-")
        option3 = tk.OptionMenu(self, var3, *optionHeads)
        option3.pack(side=tk.TOP,padx=10,pady=10)
        

        style = Style()
        style.configure('TButton', font=('Arial',10,'bold'), foreground = 'red',
        background = 'black')
        style.map('TButton', background = [('active','black')], 
        foreground = [('active', 'navy')])

##        plot_button = Button(self, text='Start Plot!', command = lambda: [controller.set_headers(var1, var2, var3),controller.show_frame(graphing_page)])
        plot_button = Button(self, text='Start Plot!', command = lambda: controller.set_headers(var1, var2, var3))
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

        global plotting_data

        if len(plotting_data)>3:
            raise Exception("You cannot plot graphs with more than 3 dimensions! Go do math mods instead!")
        elif len(plotting_data)==3:
            graph=fig.add_subplot(111, projection="3d")
        
        graph.plot(plotting_data)
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
        self.tree.place(rely=0.25,relx=0.13,relheight=0.5)
        scrlbar = Scrollbar(self,orient='vertical',command=self.tree.yview)
        # scrlbar.pack(side='right',fill='y')
        scrlbar.place(rely=0.25,relx=0.96,relheight=0.5)
        self.tree.configure(yscrollcommand=scrlbar.set)

        #Tree components
        self.tree["columns"] = ("1", "2","3")
        self.tree['show'] = 'headings'
        self.tree.column('#0', width=50, anchor='c')
        self.tree.column("1", width=100, anchor='c')
        self.tree.column("2", width=100, anchor='c')
        self.tree.column("3", width=100, anchor='c')
        self.tree.heading("1", text="Index")
        self.tree.heading("2", text="Account")
        self.tree.heading("3", text="Type")
        self.tree.bind('<ButtonRelease-1>', self.select_item)

        #Sample data values
        self.tree.insert("",'end',text="1",values=("1","Big1","Best"))
        self.tree.insert("",'end',text="2",values=("2","Big2","Best"))
        self.tree.insert("",'end',text="3",values=("3","Big3","Best"))
        self.tree.insert("",'end',text="4",values=("4","Big4","Best"))
        self.tree.insert("",'end',text="5",values=("5","Big5","Best"))
        self.tree.insert("",'end',text="6",values=("6","Big6","Best"))
        self.tree.insert("",'end',text="7",values=("7","Big7","Best"))
        self.tree.insert("",'end',text="8",values=("8","Big8","Best"))
        self.tree.insert("",'end',text="9",values=("9","Big9","Best"))
        self.tree.insert("",'end',text="10",values=("10","Big10","Best"))
        self.tree.insert("",'end',text="11",values=("11","Big11","Best"))
        self.tree.insert("",'end',text="12",values=("12","Big12","Best"))
        self.tree.insert("",'end',text="13",values=("13","Big13","Best"))
        self.tree.insert("",'end',text="14",values=("14","Big14","Best"))
        self.tree.insert("",'end',text="15",values=("15","Big15","Best"))
        self.tree.insert("",'end',text="16",values=("16","Big16","Best"))

        #Sample Tree with csv data
        self.tree["columns"] = ("1", "2","3")
        # self.tree['show'] = 'headings'
        self.tree.column('#0', width=50, anchor='c')
        self.tree.column("1", width=100, anchor='c')
        self.tree.column("2", width=100, anchor='c')
        self.tree.column("3", width=100, anchor='c')
        self.tree.heading("1", text="Date")
        self.tree.heading("2", text="Spending")
        self.tree.heading("3", text="Total")
        self.tree.bind('<ButtonRelease-1>', self.select_item)




        #Entry to input values
        # col1 = tk.Label(self,text='Column 1').place(rely=0.8,relx=0.07)
        # col2 = tk.Label(self,text='Column 2').place(rely=0.8,relx=0.38)
        # col3 = tk.Label(self,text='Column 3').place(rely=0.8,relx=0.69)

        col1 = ttk.Label(self,text='Row No.').place(rely=0.8,relx=0.07)
        col2 = ttk.Label(self,text='Column No.').place(rely=0.8,relx=0.38)
        col3 = ttk.Label(self,text='Change value into:').place(rely=0.8,relx=0.69)

        self.col1_entry = tk.Entry(self)
        self.col1_entry.place(rely=0.85,relx=0.07)
        self.col2_entry = tk.Entry(self)
        self.col2_entry.place(rely=0.85,relx=0.38)
        self.col3_entry = tk.Entry(self)
        self.col3_entry.place(rely=0.85,relx=0.69)

        print_button = ttk.Button(self, text="Print Variable", command=lambda:self.print_value(self.col1,self.col2,self.col3))
        print_button.place(rely = 0.9,relx= 0.38)

        #To insert text into entrybox
        # self.col1_entry.insert(0,some_text)

        self.col1 = tk.IntVar()
        self.col2 = tk.StringVar()
        self.col3 = tk.StringVar()

    def select_item(self, event):
        curItem = self.tree.item(self.tree.focus())
        col = self.tree.identify_column(event.x)
        print ('curItem = ', curItem)
        print ('col = ', col)
        row_value = curItem['text']

        # if col == '#0':
        #     cell_value = curItem['text']
        if col == '#1' and row_value != '':
            col_no = 1
            row_no = int(curItem['text'])
            self.col1_add_value(row_no)
            self.col1 = row_no
            self.col2_add_value(col_no)
            self.col2 = col_no
        elif col == '#2' and row_value != '':
            col_no = 2
            row_no = int(curItem['text'])
            self.col1_add_value(row_no)
            self.col1 = row_no
            self.col2_add_value(col_no)
            self.col2 = col_no
        elif col == '#3' and row_value != '':
            col_no = 3
            row_no = int(curItem['text'])
            self.col1_add_value(row_no)
            self.col1 = row_no
            self.col2_add_value(col_no)
            self.col2 = col_no

        # print ('cell_value = ', cell_value)

    def col1_add_value(self, cell_value):
        self.col1_entry.delete(0,tk.END)
        self.col1_entry.insert(0,cell_value)

    def col2_add_value(self, cell_value):
        self.col2_entry.delete(0,tk.END)
        self.col2_entry.insert(0,cell_value)

    def col3_add_value(self, cell_value):
        self.col3_entry.delete(0,tk.END)
        self.col3_entry.insert(0,cell_value)

    def print_value(self, a, b, c):
        print(a,b,c)

if __name__ == "__main__":
    app = Datatrackingapp()
    # app.geometry('400x400')
    app.update_idletasks()
    app.update()
##    app.mainloop()

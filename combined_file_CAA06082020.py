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

global variable1, variable2, variable3, selected_col, selected_row, changed_value
##global variables: variable1, variable2, variable3, data eg data[varialbe1], selected_col, selected_row, changed_value, plotting_data, plotting_vars

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

        for f in (StartPage,):
            # self.add_frame(f)
            frame = f(self.container,self) 
            self.frames[f] = frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)
        
    def set_headers(self, var1, var2, var3):

        variable1 = str(var1.get())
        variable2 = str(var2.get())
        variable3 = str(var3.get())
        
        global plotting_data
        global plotting_vars
        
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
##                print(values)
                plotting_data.append(values)

        frame = graphing_page(self.container,self)
        self.frames[graphing_page] = frame
        frame.grid(row=0,column=0,sticky="nsew")

        frame = edit_data_page(self.container,self)
        self.frames[edit_data_page] = frame
        frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(graphing_page)

    def show_edited_frame(self,values):
        frame = graphing_page(self.container,self)
        self.frames[graphing_page] = frame
        frame.grid(row=0,column=0,sticky="nsew")

        frame = edit_data_page(self.container,self)
        self.frames[edit_data_page] = frame
        frame.grid(row=0,column=0,sticky="nsew")

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
        
        save_button = ttk.Button(self, text="Save changes", command = lambda: self.save_changes())
        # save_button.pack(padx=10,pady=10)
        save_button.place(relx=0.5,rely=0.1,anchor='n')
        discard_button = ttk.Button(self, text="Discard", command = lambda: controller.show_frame(graphing_page))
        # discard_button.pack(padx=10,pady=10)
        discard_button.place(relx=0.5,rely=0.15,anchor='n')
        open_csv_button = ttk.Button(self, text="Edit File", command = lambda: controller.open_csv())
        # open_csv_button.pack(padx=10,pady=10)
        open_csv_button.place(relx=0.5,rely=0.2,anchor='n')

        #Display Data
        self.tree = Treeview(self, selectmode = 'none')
        # self.tree.pack(side='left',fill=tk.BOTH,expand=True)
        self.tree.place(rely=0.25,relx=0.13,relheight=0.5,relwidth=0.72)
        scrlbar = Scrollbar(self,orient='vertical',command=self.tree.yview)
        # scrlbar.pack(side='right',fill='y')
        scrlbar.place(rely=0.25,relx=0.96,relheight=0.5)
        self.tree.configure(yscrollcommand=scrlbar.set)

        #Check which variables are selected
        variables = []
        for variable in plotting_vars:
            if variable != '-':
                variables.append(variable)
        variable_count = len(variables)

        #Sample Tree with csv data
        self.tree.column('#0', width=50, anchor='c')
        self.tree["columns"] = variables
        for count, var in enumerate(variables):
            if count == 0:
                self.tree.column(var, width=100, anchor='c')
                self.tree.heading(var, text=str(var))
            if count == 1:
                self.tree.column(var, width=100, anchor='c')
                self.tree.heading(var, text=str(var))
            if count == 2:
                self.tree.column(var, width=100, anchor='c')
                self.tree.heading(var, text=str(var))
        self.tree.bind('<ButtonRelease-1>', self.select_item)

        with open('Spending.csv','r') as f:
            reader = csv.DictReader(f)
            count = 1

            for row in reader:
                col_count = 0
                for variable in variables:
                    if col_count == 0:
                        Col1 = row[variable]
                    elif col_count == 1:
                        Col2 = row[variable]
                    elif col_count == 2:
                        Col3 = row[variable]
                    col_count += 1
                if variable_count == 1:
                    self.tree.insert("",'end',text=str(count),values=(Col1))
                elif variable_count == 2:
                    self.tree.insert("",'end',text=str(count),values=(Col1,Col2))
                elif variable_count == 3:
                    self.tree.insert("",'end',text=str(count),values=(Col1,Col2,Col3))
                count += 1

        #Entry to input values
        col1 = tk.Label(self,text='Column 1').place(rely=0.8,relx=0.07)
        col2 = tk.Label(self,text='Column 2').place(rely=0.8,relx=0.38)
        col3 = tk.Label(self,text='Column 3').place(rely=0.8,relx=0.69)

        col1 = ttk.Label(self,text='Row No.').place(rely=0.8,relx=0.07)
        col2 = ttk.Label(self,text='Column No.').place(rely=0.8,relx=0.38)
        col3 = ttk.Label(self,text='Change value into:').place(rely=0.8,relx=0.69)

        self.row_value = tk.IntVar()
        self.col_value = tk.IntVar()
        self.input_value = tk.IntVar()

        self.col1_entry = tk.Entry(self,textvariable=self.row_value)
        self.col1_entry.place(rely=0.85,relx=0.07)
        self.col2_entry = tk.Entry(self,textvariable=self.col_value)
        self.col2_entry.place(rely=0.85,relx=0.38)
        self.col3_entry = tk.Entry(self,textvariable=self.input_value)
        self.col3_entry.place(rely=0.85,relx=0.69)

        print_button = ttk.Button(self, text="Print Variable", command=lambda:self.print_value(self.row_value,self.col_value,self.input_value))
        print_button.place(rely = 0.9,relx= 0.38)

        #To insert text into entrybox
        # self.col1_entry.insert(0,some_text)

    def edit_csv(self, filename, row_number, col_name, user_input):
        
    def edit_csv(filename, row_number, col_name, user_input):
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            values = []
            counter = 0
            for row in reader:
                if counter == row_number:
                    row[col_name] = user_input
                values.append(row)
                counter += 1

        with open(filename, "w",newline='') as file:
            writer = csv.DictWriter(file,fieldnames=headers)
            writer.writeheader()
            for value in values:
                writer.writerow(value)

    def save_changes(self):
        '''assuming you have selected_row, selected_col, and changed_value
        edit the csv here'''
        self.edit_csv('Spending.csv',selected_row,selected_col,changed_value)
        global plotting_data
##        plotting_data = edited_csv_retrieved_as_list
        controller.show_edited_frame()

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
            self.row_value = row_no
            self.col2_add_value(col_no)
            self.col_value = col_no
        elif col == '#2' and row_value != '':
            col_no = 2
            row_no = int(curItem['text'])
            self.col1_add_value(row_no)
            self.row_value = row_no
            self.col2_add_value(col_no)
            self.col_value = col_no
        elif col == '#3' and row_value != '':
            col_no = 3
            row_no = int(curItem['text'])
            self.col1_add_value(row_no)
            self.row_value = row_no
            self.col2_add_value(col_no)
            self.col_value = col_no

        global selected_col, selected_row, changed_value
        selected_col = col_no
        selected_row = row_no
        changed_value = self.input_value

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
        print(a,b,c.get())

if __name__ == "__main__":
    app = Datatrackingapp()
    # app.geometry('400x400')
    app.update_idletasks()
    app.update()
##    app.mainloop()

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:35:57 2020

@author: user
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

def get_data():
    #can change the file path to pick anohter file
    csv_data = pd.read_csv('Spending.csv', header = None)
    headers = csv_data.iloc[0]
    data = pd.DataFrame(csv_data.values[1:], columns=headers)
    #returns a pandas dataframe object
    return data


def data_selection(self, data):
    #this will appear in the data selection page
    for col in data:
        pass #for each column of data, create a checkbutton, limit the maximum number that can be selected to 3
    #create a button, that will pass the names of the checked options back to the main window (as a list of strings maybe)

def edit_csv(filename, row_number, col_name, user_input):
    #note, this assumes that headers are the first row, index 0 in all situations
    #pass the filename into here, along with the row number selected by user, and column (name of data)
    tmpFile = "tmp.csv"
    with open(filename, "r") as file, open(tmpFile, "w") as outFile:
        reader = csv.reader(file, delimiter=',')
        writer = csv.writer(outFile, delimiter=',')
        
        rownum = 0
        col_count = 0
        index = 0
        row_count = 0
        for row in reader:
            colValues = []
            #for the headers, once it iterates to the correct header, keep in mind the index
            if rownum==0:
                for col in row:
                    if col==col_name:
                        index = col_count
                    col_count += 1
                    colValues.append(col)
            else:
                for col in row:
                    colValues.append(col)
                        
            if row_count == row_number:
                colValues[index] = user_input
            row_count += 1
            writer.writerow(colValues)
        #makes a duplicate of the original file
    os.rename(tmpFile, filename)

class select_header_page(data):   
    #assuming data is a pandas dataframe
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.title = tk.title(self, "Header Selection Page")
        
        for y in range(5):
            Label(window, \
                  text="").grid(row=y, column=2)
        
        var1 = StringVar()
        Entry(window, width=12, textvariable=var1).grid(row=1, column=1)
        var2 = StringVar()
        Entry(window, width=12, textvariable=var2).grid(row=2, column=1)
        var3 = StringVar()
        Entry(window, width=12, textvariable=var3).grid(row=3, column=1)
        
        nextbutton = Button(self, \
                            bg = 'grey', \
                            fg = 'black', \
                            text="Next", \
                            command=lambda: controller.selected_header(var1, var2, var3, list(data.columns.values))).grid(row=5, column=1)
    
    def selected_header(var1, var2, var3, headers):
        try:
            datalen = 0
            relevantlist = []
            for x in [var1, var2, var3]:
                if x in headers:
                    datalen += 1
                    relevantlist.append(x)
                elif x == '':
                    continue
                else:
                    #if the value mismatch, the button will fail
                    print(0/0)
            #pass the number of variables to be used to plot, as well as relevantlist
            #relevantlist contains the names of headers to be used
            
            
            #TODO: create a function that will pass the above information ^ to the plotting page
        except:
            pass

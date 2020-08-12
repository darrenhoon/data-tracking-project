import csv

with open('New_spending.csv','r') as f:
    reader = csv.DictReader(f)
    col_headers = ['Date','Spending','Total']
    
    with open('Spending.csv','w',newline='') as newfile:
        writer = csv.DictWriter(newfile,fieldnames=col_headers)
        writer.writeheader()
        for row in reader:
##            if int(row['Spending']) == 200:
##                row['Spending'] = int(99999)
##                row['Total'] = int(99999)
##                writer.writerow(row)
##            else:
            writer.writerow(row)

##with open('Spending.csv','r') as file:
##    reader = csv.DictReader(file)
##    col_headers = ['Date','Spending','Total']
##    values = []
##
##    for row in reader:
####        if int(row['Spending']) == 200:
####            row['Spending'] = 99999
####            row['Total'] = 99999
####            values.append(row)
####        else:
##        values.append(row)
##file.close()
##
##with open('Spending.csv','w',newline='') as file:
##    writer = csv.DictWriter(file,fieldnames=col_headers)
##    writer.writeheader()
##    for value in values:
##        writer.writerow(value)
        

            


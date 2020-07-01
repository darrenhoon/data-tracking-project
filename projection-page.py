import Tkinter as tk
from Tkinter import tkk
import tkFont
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class page_two:
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        title = tk.title(self, "Plot Page")

        ##this part can be edited if we do not want underline for the whole heading
        text = tk.Label(text="Plotting Page", font=("Arial",12)))
        text.pack()
        heading= tkFont.Font(text, text.cget("font"))
        text.configure(underline = True)
        heading.configure(font=text)

        # if the above underliing causes issues, use the below code which has no underline
        # label = tk.label(self, text="Plotting Page", font=("Arial",12))
        # label.pack(pady=500,padx=500)

        back_button = tkk.Button(self, text="Back to Main Menu", command = lambda: controller.showFrame(Main_Menu))
        #the Main_Menu to be changed based on what the main menu class is going to be
        back_button.pack()

        fig = Figure(figsize(5,5), dpi=100) #backend to generate the window
        graph=fig.add_subsplot(1,1,1)

        ##INSERT DATA EXTRACTED FROM CSV HERE
        # data = 
        page = FigureCanvasTkAgg(fig,self)
        page.show()
        page.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)


        #toolbar page, for futher applications to edit saved data
        toolbar=NavigationToolbar2Tk(page,self)
        toolbar.update()
        page.tkcanvas.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)




##probably in the final py file rather than here to start the programme
# root = tk.Tk()
# gui=page_two(root)
# root.mainloop()
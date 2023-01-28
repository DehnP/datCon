import tkinter
from tkinter import filedialog
from matplotlib.figure import Figure
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
from datFuncs import *
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set appearance mode and default color theme
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.resizable(0,0)
        self.title("datConv")
        self.iconbitmap("Assets/datCon.ico")
        # initialize the window
        self.view1()

    def view1(self):
        customFont = ('Arciform',12)
        #==========FRAMING===========
        self.f1 = ctk.CTkFrame(self)
        self.f1.grid(row=0,column=0,pady=10,padx=10)
        self.f2 = ctk.CTkFrame(self)
        self.f2.grid(row=1,column=0,pady=10,padx=10)

        #==========FRAME 1===========
        self.folder_icon = ctk.CTkImage(light_image=Image.open("Assets/Folder.png"))
        self.File_Loc_Label = ctk.CTkLabel(self.f1,text='File Location',font=customFont)
        self.File_Loc_Label.grid(row=0,column=0,columnspan=3,sticky='nsew',pady=2)

        self.File_Loc_Entry = ctk.CTkEntry(self.f1,placeholder_text='C:\\..',width=300)
        self.File_Loc_Entry.grid(row=1,column=0,sticky='nsew',pady=2,columnspan=2)

        self.File_Loc_Open = ctk.CTkButton(self.f1,text='',width=20,image=self.folder_icon,command=self.openFile)
        self.File_Loc_Open.grid(row=1,column=2,sticky='nsew',pady=2)

        self.Chord_Label = ctk.CTkLabel(self.f1,text='Chord Length',font=customFont)
        self.Chord_Label.grid(row=2,column=0,sticky='nsew',pady=2)

        self.Chord_Entry = ctk.CTkEntry(self.f1,placeholder_text='160..')
        self.Chord_Entry.grid(row=3,column=0,sticky='nsew',pady=2)

        self.Button_load = ctk.CTkButton(self.f1,text='Load',width=50,command=self.loadButton)
        self.Button_load.grid(row=2,column=1,sticky='nsew',pady=2,columnspan=2)

        self.Button_plot = ctk.CTkButton(self.f1,text='Plot',width=50,command=self.plotButton)
        self.Button_plot.grid(row=3,column=1,sticky='nsew',pady=2,columnspan=2)



        #==========FRAME 2===========
        self.Save_Loc_Label = ctk.CTkLabel(self.f2,text='Save Location')
        self.Save_Loc_Label.grid(row=0,column=0,columnspan=3,sticky='nsew',pady=2)

        self.Save_Loc_Entry = ctk.CTkEntry(self.f2,placeholder_text='D:\\..',width=300)
        self.Save_Loc_Entry.grid(row=1,column=0,sticky='nsew',pady=2,columnspan=2)

        self.Save_Loc_Open = ctk.CTkButton(self.f2,text='',width=20,image=self.folder_icon,command=self.saveFile)
        self.Save_Loc_Open.grid(row=1,column=3,sticky='nsew',pady=2) 

        self.File_Name_Label = ctk.CTkLabel(self.f2,text='File Name')
        self.File_Name_Label.grid(row=2,column=0,sticky='nsew',pady=2)


        self.File_Name_Entry = ctk.CTkEntry(self.f2,placeholder_text='NACAXXXX..')
        self.File_Name_Entry.grid(row=3,column=0,sticky='nsew',pady=2)


        self.File_Save = ctk.CTkButton(self.f2,text='Save',width=50,command=self.saveButton)
        self.File_Save.grid(row=3,column=1,columnspan=3,sticky='nsew') 

        self.quitButton = ctk.CTkButton(self.f2,text='Quit',command = self.quitProgram)
        self.quitButton.grid(row=4,column=1,columnspan=3,sticky='nsew',pady=5)

    #==========METHODS===========
    def openFile(self):
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window
        tempdir = filedialog.askopenfilename(parent=root, title='Please select a file',filetypes=[('Text file','.txt'),('.dat file','.dat')])
        # Insert file path into entry box
        if len(tempdir) > 0:
            self.File_Loc_Entry.delete(0,'end')
            self.File_Loc_Entry.insert(0, tempdir)

    def loadButton(self):
        if self.Chord_Entry.get().isdigit():
            array = strip_txt_to_array(self.File_Loc_Entry.get())
            array = add_ones(array)
            array = multiply_by_chord_length(int(self.Chord_Entry.get()),array)
            global arr
            arr = array
        else:
            print('Enter a chord length & file path')

    def plotButton(self):
        if 'arr' in globals():
            fig = Figure(figsize=(6.5,3),dpi=100)
            fig.set_facecolor('xkcd:black')
            x = arr[:,1]
            y = arr[:,2]
            plot1 = fig.add_subplot(111)
            plot1.plot(x,y)
            canvas = FigureCanvasTkAgg(fig)
            canvas.get_tk_widget().grid(row=0,column=1,rowspan=3)

        else:
            print('Load a file first..')

    def saveFile(self):
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window
        tempdir = filedialog.askdirectory(parent=root, title='Please select a folder')
        if len(tempdir) > 0:
            self.Save_Loc_Entry.delete(0,'end')
            self.Save_Loc_Entry.insert(0, tempdir)

    def saveButton(self):
        if len(self.Save_Loc_Entry.get()) > 0:
            savePath = (self.Save_Loc_Entry.get()+'\\'+self.File_Name_Entry.get()+'.txt')
            np.savetxt(savePath,arr,fmt='%1.6f',delimiter=',')
            var = prepend_line_to_file(savePath,'polyline=true')
            remove_decimal_zeros(savePath)
            print('File saved to: '+savePath)
        else:
            print('')


    def quitProgram(self):
        App.destroy(self)
        App.quit(self)


if __name__ == "__main__":
  app = App()
  app.mainloop()

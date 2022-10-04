import tkinter
from tkinter import filedialog
from matplotlib.figure import Figure
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
from datfuncs2 import OpenTextFile, AddOnes, chordMult, prepend_line


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.geometry(f"{345}x{350}")
        self.resizable(0,0)
        self.title(".dat Converter 2")
        self.view1()

    def view1(self):

        #==========FRAMING===========
        self.f1 = ctk.CTkFrame(self)
        self.f1.grid(row=0,column=0,pady=10,padx=10)
        self.f2 = ctk.CTkFrame(self)
        self.f2.grid(row=2,column=0,pady=10,padx=10)

        #==========FRAME 1===========
        photo = tkinter.PhotoImage(file = "D:\PythonPlayground\datConverter2\Assets\Folder.png")
        self.File_Loc_Label = ctk.CTkLabel(self.f1,text='File Location')
        self.File_Loc_Label.grid(row=0,column=0,columnspan=3,sticky='nsew',pady=2)

        self.File_Loc_Entry = ctk.CTkEntry(self.f1,placeholder_text='D:\\..',width=300)
        self.File_Loc_Entry.grid(row=1,column=0,sticky='nsew',pady=2,columnspan=2)

        self.File_Loc_Open = ctk.CTkButton(self.f1,text='',width=20,image=photo,command=self.openFile)
        self.File_Loc_Open.grid(row=1,column=2,sticky='nsew',pady=2)

        self.Chord_Label = ctk.CTkLabel(self.f1,text='Chord Length')
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

        self.Save_Loc_Open = ctk.CTkButton(self.f2,text='',width=20,image=photo,command=self.saveFile)
        self.Save_Loc_Open.grid(row=1,column=3,sticky='nsew',pady=2) 

        self.File_Name_Label = ctk.CTkLabel(self.f2,text='File Name')
        self.File_Name_Label.grid(row=2,column=0,sticky='nsew',pady=2)


        self.File_Name_Entry = ctk.CTkEntry(self.f2,placeholder_text='NACAXXXX..')
        self.File_Name_Entry.grid(row=3,column=0,sticky='nsew',pady=2)


        self.File_Save = ctk.CTkButton(self.f2,text='Save',width=50,command=self.saveButton)
        self.File_Save.grid(row=3,column=1,columnspan=3,sticky='nsew') 

        self.quitButton = ctk.CTkButton(self.f2,text='Quit',command = self.quitProgram)
        self.quitButton.grid(row=4,column=1,columnspan=3,sticky='nsew',pady=5)


    def view2(view1):
        view1.f3 = tkinter.Frame(view1)
        view1.f3.grid(row=1,column=0)

        view1.label = ctk.CTkLabel(view1.f3,text='REEEEEEEE',width=310,height=120)
        view1.label.pack(pady=10,padx=10)

    def openFile(self):
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window
        print("openfileexplorer")
        tempdir = filedialog.askopenfilename(parent=root, title='Please select a file')
        if len(tempdir) > 0:
            self.File_Loc_Entry.delete(0,'end')
            self.File_Loc_Entry.insert(0, tempdir)

    def loadButton(self):
        if self.Chord_Entry.get().isdigit():
            array = OpenTextFile(self.File_Loc_Entry.get())
            array = AddOnes(array)
            array = chordMult(int(self.Chord_Entry.get()),array)
            global arr
            arr = array
        else:
            print('Enter a chord length & file path, idiot.')

    def plotButton(self):
        if 'arr' in globals():
            self.view2
            fig = Figure(figsize=(5,5),dpi=100)
            x = arr[:,1]
            y = arr[:,2]
            plot1 = fig.add_subplot(111)
            plot1.plot(x,y)
            canvas = FigureCanvasTkAgg(fig,self.f3)
            canvas.get_tk_widget().pack()

        else:
            print('Load a file first..')

    def saveFile(self):
        print("savefolderexplorer")
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window
        tempdir = filedialog.askdirectory(parent=root, title='Please select a folder')
        if len(tempdir) > 0:
            self.Save_Loc_Entry.delete(0,'end')
            self.Save_Loc_Entry.insert(0, tempdir)

    def saveButton(self):
        np.savetxt(self.Save_Loc_Entry.get()+'\\'+self.File_Name_Entry.get()+'.txt',arr,fmt='%1.6f',delimiter='  ')
        var = prepend_line(self.Save_Loc_Entry.get()+'\\'+self.File_Name_Entry.get()+'.txt','Polyline=true')


    def quitProgram(self):
        App.destroy(self)
        App.quit(self)


if __name__ == "__main__":
  app = App()
  app.mainloop()
import tkinter
from tkinter import filedialog
from matplotlib.figure import Figure
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np
from datFuncs3D import *
from datConvClasses import *
from PIL import Image
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set appearance mode and default color theme
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.resizable(0,0)
        self.geometry("1000x600")
        self.title("datConv")
        self.iconbitmap("Assets/datCon.ico")
        # initialize the window
        self.mainView()


    def mainView(self):
        titlesFont = ctk.CTkFont(family="Arciform", size=20)
        textFont = ctk.CTkFont(family="Arciform", size=12)
        ##=====================FRAMING==================================================
        self.masterFrame = ctk.CTkFrame(self)
        self.masterFrame.pack(pady=5,padx=5,fill='both',expand=True)

        self.rightFrame = ctk.CTkFrame(self.masterFrame)
        self.rightFrame.pack(side='right',fill='both',expand=True,padx=5,pady=5)
        #===============================================================================

        ##=====================leftFrame==================================================
        self.tabView = ctk.CTkTabview(self.masterFrame)
        self.tabView.pack(fill='both',expand=True,padx=5,pady=5,side='left')
        self.configTab = self.tabView.add("Config")
        self.saveTab = self.tabView.add("Save/Load")

        #=====================Config==================================================
        self.configFrame = ctk.CTkFrame(self.configTab)
        self.configFrame.pack(fill='both',expand=True,padx=5,pady=5)

        ## Config Widgets
        self.profileFrame = ctk.CTkFrame(self.configFrame)
        self.profileFrame.pack(fill='x',expand=True,padx=5,pady=5,anchor='n')

        # section quantity
        self.num_of_profiles_INT = 1
        self.sectionQuantityLabel = ctk.CTkLabel(self.profileFrame,text="Number of sections: ",font=textFont)
        self.sectionQuantityLabel.pack(side='left',padx=5,pady=5)
        self.sectionQuantityEntry = ctk.CTkEntry(self.profileFrame,font=textFont,width=55)
        self.sectionQuantityEntry.pack(side='left',padx=5,pady=5)
        self.sectionQuantityEntry.insert(0,"1")

        # profile displacement
        self.profileDisplacementLabel = ctk.CTkLabel(self.profileFrame,text="Displacement",font=textFont)
        self.profileDisplacementLabel.pack(side='left',padx=5,pady=5)
        self.profileDisplacementEntry = ctk.CTkEntry(self.profileFrame,font=textFont,width=55)
        self.profileDisplacementEntry.pack(side='left',padx=5,pady=5)
        self.profileDisplacementEntry.insert(0,"0")

        # set button
        self.setButton = ctk.CTkButton(self.profileFrame,text="Set",font=textFont,command=self.change_number_of_profile_event)
        self.setButton.pack(side='right',padx=5,pady=5)

        # profile config frame
        self.profileConfigFrame = ctk.CTkFrame(self.configFrame)
        self.profileConfigFrame.pack(fill='x',expand=True,padx=5,pady=5,anchor='n')

        # section select
        self.sectionSelectLabel = ctk.CTkLabel(self.profileConfigFrame,text="Section: ",font=textFont)
        self.sectionSelectLabel.pack(side='left',padx=5,pady=5)
        self.sectionSelectOption = ctk.CTkOptionMenu(self.profileConfigFrame,values=["1"],font=textFont,width=55)
        self.sectionSelectOption.pack(side='left',padx=5,pady=5)
        self.sectionSelectOption.set(1)

        # profile Twist
        self.profileTwistLabel = ctk.CTkLabel(self.profileConfigFrame,text="Twist: ",font=textFont)
        self.profileTwistLabel.pack(side='left',padx=5,pady=5)
        self.profileTwistEntry = ctk.CTkEntry(self.profileConfigFrame,font=textFont,width=55)
        self.profileTwistEntry.pack(side='left',padx=5,pady=5)
        self.profileTwistEntry.insert(0,"0")

        # profile Chord
        self.profileChordLabel = ctk.CTkLabel(self.profileConfigFrame,text="Chord: ",font=textFont)
        self.profileChordLabel.pack(side='left',padx=5,pady=5)
        self.profileChordEntry = ctk.CTkEntry(self.profileConfigFrame,font=textFont,width=55)
        self.profileChordEntry.pack(side='left',padx=5,pady=5)
        self.profileChordEntry.insert(0,"1")

        # profile select
        self.profileSelectLabel = ctk.CTkLabel(self.profileConfigFrame,text="Profile: ",font=textFont)
        self.profileSelectLabel.pack(side='left',padx=5,pady=5)

        # list of profile txt files in the profile folder
        self.listProfiles()


        self.profileSelectOption = ctk.CTkOptionMenu(self.profileConfigFrame,values=self.profileList,font=textFont,width=55)
        self.profileSelectOption.pack(side='left',padx=5,pady=5)
        self.profileSelectOption.set("")

        # profile save button
        self.profileSaveButton = ctk.CTkButton(self.profileConfigFrame,text="Save",font=textFont,command=self.save_section_config_event)
        self.profileSaveButton.pack(side='right',padx=5,pady=5)





        #=====================Save/Load==================================================
        self.saveLoadFrame = ctk.CTkFrame(self.saveTab)
        self.saveLoadFrame.pack(fill='both',expand=True,padx=5,pady=5)

        ## Save/Load Widgets
        self.saveLoadFrame = ctk.CTkFrame(self.saveLoadFrame)
        self.saveLoadFrame.pack(fill='both',expand=True,padx=5,pady=5)

        self.folder_icon = ctk.CTkImage(light_image=Image.open("Assets/Folder.png"))
        self.File_Loc_Label = ctk.CTkLabel(self.saveLoadFrame,text='File Location')
        self.File_Loc_Label.grid(row=0,column=0,columnspan=3,sticky='nsew',pady=2)

        self.File_Loc_Entry = ctk.CTkEntry(self.saveLoadFrame,placeholder_text='C:\\..',width=300)
        self.File_Loc_Entry.grid(row=1,column=0,sticky='nsew',pady=2,columnspan=2)
        
        self.File_Loc_Open = ctk.CTkButton(self.saveLoadFrame,text='',width=20,image=self.folder_icon,command=self.open_file_location_event)
        self.File_Loc_Open.grid(row=1,column=2,sticky='nsew',pady=2)


        self.File_Name_Label = ctk.CTkLabel(self.saveLoadFrame,text='File Name')
        self.File_Name_Label.grid(row=2,column=0,sticky='nsew',pady=2)


        self.File_Name_Entry = ctk.CTkEntry(self.saveLoadFrame,placeholder_text='NACAXXXX..')
        self.File_Name_Entry.grid(row=3,column=0,sticky='nsew',pady=2)


        self.File_Save = ctk.CTkButton(self.saveLoadFrame,text='Save',width=50,command=self.save_profile_event)
        self.File_Save.grid(row=3,column=1,columnspan=3,sticky='nsew') 
            

        ##=====================rightFrame==================================================
        self.plotViewLabel = ctk.CTkLabel(self.rightFrame,text="Plot View",font=titlesFont)
        self.plotViewLabel.pack(side='top',padx=5,pady=5)
 
        self.plotViewFrame = ctk.CTkFrame(self.rightFrame)
        self.plotViewFrame.pack(fill='both',expand=True,padx=10,pady=10)

    def change_number_of_profile_event(self):
        print("change_number_of_profile_event")
        # get value from profile quantity entry
        self.num_of_profiles_INT = int(self.sectionQuantityEntry.get())
        options = [str(i) for i in range(1, self.num_of_profiles_INT+1)]
        # update the options in the profile select option menu
        self.sectionSelectOption.configure(values=options)

    def save_section_config_event(self):
        # Save configuration of section
        print("save_profile_event")

    def load_profile_event(self):
        # load dat file
        print("load_profile_event")
        

    def open_file_location_event(self):
        # open file location
        print("open_file_location_event")
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window
        tempdir = filedialog.askopenfilename(parent=root, title='Please select a file',filetypes=[('Text file','.txt'),('.dat file','.dat')])
        # Insert file path into entry box
        if len(tempdir) > 0:
            self.File_Loc_Entry.delete(0,'end')
            self.File_Loc_Entry.insert(0, tempdir)

    def save_profile_event(self):
        # save profile to /Profiles
        if len(self.File_Name_Entry.get()) == 0:
            print("No File Name")
            return
        else:
            array = strip_txt_to_array(self.File_Loc_Entry.get())
            savePath = ("Profiles/"+self.File_Name_Entry.get()+".txt")
            np.savetxt(savePath, array,fmt='%1.6f',delimiter=",")

    def listProfiles(self):
        # list all profiles in the profile folder
        self.profileList = []
        for file in os.listdir("Profiles"):
            if file.endswith(".txt"):
                self.profileList.append(file.replace(".txt",""))


        
if __name__ == "__main__":
  app = App()
  app.mainloop()

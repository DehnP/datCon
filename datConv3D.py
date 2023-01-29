import tkinter
from tkinter import filedialog
from matplotlib.figure import Figure
import customtkinter as ctk
import numpy as np
from datFuncs3D import *
from PIL import Image
import os
from dataclasses import dataclass
import pickle
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Blade:
    def __init__(self,sections=[]):
        self.sections = sections # list of sections
    
    def add_section(self, section):
        # check if a section with the same n value exists
        for i, s in enumerate(self.sections):
            if s.n == section.n:
                self.sections.pop(i) # remove existing section
                break
        self.sections.append(section) # add new section to list of sections

@dataclass
class Section:
    n: int# section number
    dr: float # displacement
    twist: float# twist angle
    chord: float# chord length
    profile: np.array# profile coordinates
    coords: np.array# 3D coordinates

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # set appearance mode and default color theme
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        self.resizable(0,0)
        # self.geometry("1000x600")
        self.title("datConv")
        self.iconbitmap("Assets/datCon.ico")
        # initialize the window
        self.mainView()
        self.currentBlade = Blade()

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
        self.importTab = self.tabView.add("Import")

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
        self.sectionTwistLabel = ctk.CTkLabel(self.profileConfigFrame,text="Twist: ",font=textFont)
        self.sectionTwistLabel.pack(side='left',padx=5,pady=5)
        self.sectionTwistEntry = ctk.CTkEntry(self.profileConfigFrame,font=textFont,width=55)
        self.sectionTwistEntry.pack(side='left',padx=5,pady=5)
        self.sectionTwistEntry.insert(0,"0")

        # profile Chord
        self.sectionChordLabel = ctk.CTkLabel(self.profileConfigFrame,text="Chord: ",font=textFont)
        self.sectionChordLabel.pack(side='left',padx=5,pady=5)
        self.sectionChordEntry = ctk.CTkEntry(self.profileConfigFrame,font=textFont,width=55)
        self.sectionChordEntry.pack(side='left',padx=5,pady=5)
        self.sectionChordEntry.insert(0,"1")

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

        # save Blade Frame
        self.saveBladeFrame = ctk.CTkFrame(self.configFrame)
        self.saveBladeFrame.pack(fill='x',expand=True,padx=5,pady=5,anchor='n')
        
        # save Blade Button
        self.saveBladeButton = ctk.CTkButton(self.saveBladeFrame,text="Save Blade",font=textFont,command=self.save_blade_event)
        self.saveBladeButton.pack(side='right',padx=5,pady=5)

        # save Blade Name Entry
        self.saveBladeNameEntry = ctk.CTkEntry(self.saveBladeFrame,font=textFont,width=100)
        self.saveBladeNameEntry.pack(side='right',padx=5,pady=5)
        self.saveBladeNameEntry.insert(0,"Blade Name")

        # plot Blade Frame
        self.plotBladeFrame = ctk.CTkFrame(self.configFrame)
        self.plotBladeFrame.pack(fill='x',expand=True,padx=5,pady=5,anchor='n')
        # plot Blade Button
        self.plotBladeButton = ctk.CTkButton(self.plotBladeFrame,text="Plot Blade",font=textFont,command=self.plot_blade_event)
        self.plotBladeButton.pack(side='right',padx=5,pady=5)

        # load Blade Frame
        self.loadBladeFrame = ctk.CTkFrame(self.configFrame)
        self.loadBladeFrame.pack(fill='x',expand=True,padx=5,pady=5,anchor='n')
        # load Blade Button
        self.loadBladeButton = ctk.CTkButton(self.loadBladeFrame,text="Load Blade",font=textFont,command=self.load_blade_event)
        self.loadBladeButton.pack(side='right',padx=5,pady=5)


        #=====================Save/Load==================================================
        self.saveLoadFrame = ctk.CTkFrame(self.importTab)
        self.saveLoadFrame.pack(fill='both',expand=True,padx=5,pady=5)

        ## Save/Load Widgets
        self.saveLoadFrame = ctk.CTkFrame(self.saveLoadFrame)
        self.saveLoadFrame.pack(fill='both',expand=True,padx=5,pady=5)

        self.folder_icon = ctk.CTkImage(light_image=Image.open("Assets/Folder.png"))
        self.File_Loc_Label = ctk.CTkLabel(self.saveLoadFrame,text='Import .dat File Location:')
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
            
        self.Save_Loc_Label = ctk.CTkLabel(self.saveLoadFrame,text='Export SC compatible Save Location:')
        self.Save_Loc_Label.grid(row=4,column=0,columnspan=3,sticky='nsew',pady=2)

        self.Save_Loc_Entry = ctk.CTkEntry(self.saveLoadFrame,placeholder_text='D:\\..',width=300)
        self.Save_Loc_Entry.grid(row=5,column=0,sticky='nsew',pady=2,columnspan=2)

        self.Save_Loc_Open = ctk.CTkButton(self.saveLoadFrame,text='',width=20,image=self.folder_icon,command=self.open_save_location_event)
        self.Save_Loc_Open.grid(row=5,column=2,sticky='nsew',pady=2) 

        self.File_Name_Label = ctk.CTkLabel(self.saveLoadFrame,text='File Name')
        self.File_Name_Label.grid(row=6,column=0,sticky='nsew',pady=2)


        self.File_Name_Entry = ctk.CTkEntry(self.saveLoadFrame,placeholder_text='NACAXXXX..')
        self.File_Name_Entry.grid(row=7,column=0,sticky='nsew',pady=2)


        self.File_Save = ctk.CTkButton(self.saveLoadFrame,text='Save',width=50,command=self.export_curves_event)
        self.File_Save.grid(row=7,column=1,columnspan=3,sticky='nsew') 


        ##=====================rightFrame==================================================
        self.plotViewLabel = ctk.CTkLabel(self.rightFrame,text="Plot View",font=titlesFont)
        self.plotViewLabel.pack(side='top',padx=5,pady=5)
 
        self.plotViewFrame = ctk.CTkFrame(self.rightFrame)
        self.plotViewFrame.pack(fill='both',expand=True,padx=10,pady=10)

##=====================METHODS==================================================
    def open_save_location_event(self):
        root = tkinter.Tk()
        root.withdraw() #use to hide tkinter window
        tempdir = filedialog.askdirectory(parent=root, title='Please select a folder')
        if len(tempdir) > 0:
            self.Save_Loc_Entry.delete(0,'end')
            self.Save_Loc_Entry.insert(0, tempdir)

    def export_curves_event(self):
        # Export curves to SC compatible format
        print("export_curves_event")
        
        # create temp array
        tempArray = np.array(self.currentBlade.sections[0].coords)
        tempFullArray = tempArray

        # read rest of sections and add to tempFullArray
        for i in range(1,len(self.currentBlade.sections)):
            tempArray = np.array(self.currentBlade.sections[i].coords)
            # append to tempFullArray
            tempFullArray = np.concatenate((tempFullArray, tempArray), axis=0)
        print(tempFullArray)
        # round values in tempFullArray to 8 decimal places
        tempFullArray = np.around(tempFullArray, decimals=8)

        # save to file
        np.savetxt(self.Save_Loc_Entry.get() + "\\" + self.File_Name_Entry.get() + ".txt", tempFullArray, delimiter=",",fmt='%.6f')
        add_blank_line(self.Save_Loc_Entry.get() + "\\" + self.File_Name_Entry.get() + ".txt")
        prepend_line_to_file(self.Save_Loc_Entry.get() + "\\" + self.File_Name_Entry.get() + ".txt", "3d=true")
    
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
        # get values from entry boxes
        sectionIndex = int(self.sectionSelectOption.get())
        sectionDisplacement = float(self.profileDisplacementEntry.get())
        sectionTwist = float(self.sectionTwistEntry.get())
        sectionChord = float(self.sectionChordEntry.get())
        # strip the .txt from the profile name
        tempProfileName = self.profileSelectOption.get()
        sectionProfile = strip_profile_to_array("Profiles/" + tempProfileName + ".txt")

        # generate coords for profile
        sectionCoords = scale_profile(sectionProfile,sectionChord)
        sectionCoords = rotate_profile(sectionCoords,sectionTwist)
        sectionCoords = add_displacement_column(sectionCoords,sectionIndex,sectionDisplacement)

        # save to class 'section' object
        tempSec = Section(sectionIndex,sectionDisplacement,sectionTwist,sectionChord,sectionProfile,sectionCoords)

        # save to class 'blade' object
        self.currentBlade.add_section(tempSec)

        print(tempSec)
        print(self.currentBlade.sections)


    def save_blade_event(self):
        # save blade to file
        print("save_blade_event")
        # get blade name from entry box
        bladeName = self.saveBladeNameEntry.get()
        with open('Blades/' + bladeName + '.txt', 'wb') as f:
            pickle.dump(self.currentBlade, f)

    def load_blade_event(self):
        # load blade from file
        print("load_blade_event")
        root = tkinter.Tk()
        root.withdraw()
        tempdir = filedialog.askopenfilename(parent=root, title='Please select a file',filetypes=[('Text file','.txt')])
        if len(tempdir) > 0:
            with open(tempdir, 'rb') as f:
                self.currentBlade = pickle.load(f)
    

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
            array = strip_dat_to_array(self.File_Loc_Entry.get())
            savePath = ("Profiles/"+self.File_Name_Entry.get()+".txt")
            np.savetxt(savePath, array,fmt='%1.6f',delimiter=",")

    def listProfiles(self):
        # list all profiles in the profile folder
        self.profileList = []
        for file in os.listdir("Profiles"):
            if file.endswith(".txt"):
                self.profileList.append(file.replace(".txt",""))

    def plot_blade_event(self):
        # plot blade
        print("plot_blade_event")
        # concatenate all sections
        bladeCoords = np.array([])
        for section in self.currentBlade.sections:
            if bladeCoords.size == 0:
                bladeCoords = section.coords
            else:
                bladeCoords = np.concatenate((bladeCoords,section.coords),axis=0)
                
        ## plot 3d blade on plotView canvas 
        # clear canvas
        self.plotViewFrame.destroy()
        self.plotViewFrame = ctk.CTkFrame(self.rightFrame)
        self.plotViewFrame.pack(fill='both',expand=True,padx=10,pady=10)
        # plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(bladeCoords[:,0],bladeCoords[:,1],bladeCoords[:,2])
        # keep axes equal
        max_range = np.array([bladeCoords[:,0].max()-bladeCoords[:,0].min(), bladeCoords[:,1].max()-bladeCoords[:,1].min(), bladeCoords[:,2].max()-bladeCoords[:,2].min()]).max() / 2.0
        mid_x = (bladeCoords[:,0].max()+bladeCoords[:,0].min()) * 0.5
        mid_y = (bladeCoords[:,1].max()+bladeCoords[:,1].min()) * 0.5
        mid_z = (bladeCoords[:,2].max()+bladeCoords[:,2].min()) * 0.5
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        # plot on canvas
        canvas = FigureCanvasTkAgg(fig, master=self.plotViewFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.plotViewFrame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)





        
if __name__ == "__main__":
  app = App()
  app.mainloop()

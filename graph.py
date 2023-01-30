from classes import *
import customtkinter as ctk
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use('TkAgg')


def plot_blade_event(current_blade: Blade, master_frame, plot_view_frame) -> None:
    # plot blade
    print("plot_blade_event")
    # concatenate all sections
    blade_coords = np.array([])
    for Section in current_blade.sections:
        if blade_coords.size == 0:
            blade_coords = Section.coords
            print('----test----')
            print(blade_coords)
        else:
            blade_coords = np.concatenate(
                (blade_coords, Section.coords), axis=0)

    print(blade_coords)
    # plot 3d blade on plotView canvas
    # clear canvas
    plot_view_frame.destroy()
    plot_view_frame = ctk.CTkFrame(master_frame)
    plot_view_frame.pack(fill='both', expand=True, padx=10, pady=10)
    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(blade_coords[:, 0], blade_coords[:, 1], blade_coords[:, 2])
    # keep axes equal
    max_range = np.array([blade_coords[:, 0].max()-blade_coords[:, 0].min(), blade_coords[:, 1].max(
    )-blade_coords[:, 1].min(), blade_coords[:, 2].max()-blade_coords[:, 2].min()]).max() / 2.0
    mid_x = (blade_coords[:, 0].max()+blade_coords[:, 0].min()) * 0.5
    mid_y = (blade_coords[:, 1].max()+blade_coords[:, 1].min()) * 0.5
    mid_z = (blade_coords[:, 2].max()+blade_coords[:, 2].min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    # plot on canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_view_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, plot_view_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

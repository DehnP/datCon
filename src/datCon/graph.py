from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from classes import *
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


def plot_blade_event(current_blade: Blade, plot_frame) -> None:
    for widget in plot_frame.winfo_children():
        widget.destroy()
    blade_coords = np.concatenate(
        [section.coords for section in current_blade.sections], axis=0)

    plot_view_frame = tk.Frame(plot_frame)
    plot_view_frame.pack(fill='both', expand=True, padx=10, pady=10)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    distances = np.linalg.norm(np.diff(blade_coords, axis=0), axis=1)
    mean_distance = np.mean(distances)
    std_distance = np.std(distances)
    # adjust the number of standard deviations as desired
    threshold = mean_distance + 3 * std_distance

    for i in range(len(blade_coords) - 1):
        if distances[i] <= threshold:
            x = [blade_coords[i, 0], blade_coords[i + 1, 0]]
            y = [blade_coords[i, 1], blade_coords[i + 1, 1]]
            z = [blade_coords[i, 2], blade_coords[i + 1, 2]]
            ax.plot(x, y, z, linestyle='solid')

    max_range = max(blade_coords.max(axis=0) - blade_coords.min(axis=0)) / 2
    mid = blade_coords.mean(axis=0)
    ax.set_xlim(mid[0] - max_range, mid[0] + max_range)
    ax.set_ylim(mid[1] - max_range, mid[1] + max_range)
    ax.set_zlim(mid[2] - max_range, mid[2] + max_range)

    canvas = FigureCanvasTkAgg(fig, master=plot_view_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, plot_view_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

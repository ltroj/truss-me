# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 23:20:44 2017

@author: Lukas
"""

from trussme import truss
import Tkinter as tk
import tkFileDialog
import os
import datetime


def import_data():
    root = tk.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
    return file_path

if __name__ == "__main__":
    file_path = import_data()

    # Build truss from file
    t = truss.Truss(file_path)
    t.set_goal(min_fos_buckling=1.5,
               min_fos_yielding=1.5,
               max_mass=5.0,
               max_deflection=6e-3)
    # Save report

    # A C H T U N G: Derzeit wird OHNE Report nichts berechnet,
    # entsprechend stimmt auch der Plot nicht
    timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    t.print_and_save_report(os.path.join(os.path.dirname(__file__),
                            'report_'+base_name+'_'+timestamp+'.txt'))
    # Plot truss
    t.plot(mlbl=True, jlbl=True, ldlbl=True, legend=True)

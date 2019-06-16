import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
import os

# Main GUI

window =  tk.Tk()
#window.geometry('800x600')
window.title('QBSO-FS')
window.iconbitmap('media/bee.ico')
gamma = 0.5

# Frames init

param_frame = tk.Frame(window)
param_frame.grid(column=0,row=0)

lb_QL = tk.Label(param_frame,text="Paramètres du Q-Learning")
lb_alpha = tk.Label(param_frame,text='alpha')
etr_alpha = tk.Entry(param_frame,text='0.1')
lb_alpha.grid(column=0,row=1)
etr_alpha.grid(column=1,row=1)

# lb_BSO = tk.Label(param_frame,text="Paramètres du BSO")
# lb_BSO.grid(column=2,row=0)

# lb_Classifiers = tk.Label(param_frame,text="Paramètres des Classifieurs")
# lb_Classifiers.grid(column=4,row=0)

# test_frame = tk.Frame(window)
# test_frame.grid(column=0,row=4)
# results_frame = tk.Frame(window)
# results_frame.grid(column=0,row=8)



# Datasets

# datasets = []
# dir_path = os.path.dirname(os.path.realpath(__file__))
# mypath = dir_path = os.path.dirname(os.path.realpath(__file__)) + "/datasets/"
# for (dirpath, dirnames, filenames) in os.walk(mypath):
#     datasets.extend(filenames)
#     break

# combo_datasets = ttk.Combobox(test_frame)
# combo_datasets['values'] = datasets




# # Methods




# # Widgets 

# btn =  tk.Button(test_frame,text="Ok")
# label = tk.Label(text=str(gamma))
# value = tk.DoubleVar(test_frame)
# sb_gamma = tk.Spinbox(test_frame, textvariable=value, from_=0.80, to=0.99, increment=0.05)








# # Positioning
# sb_gamma.grid(row=0, column=0)
# label.grid(row=1, column=0)
# btn.grid(row=2, column=0)
# combo_datasets.grid(row=4, column=0)

# Launch GUI

window.mainloop()

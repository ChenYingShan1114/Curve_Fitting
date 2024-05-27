import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from do_curvefit import do_curvefit
root = tk.Tk()
root.title('Fitting!!')
root.geometry('1000x700')
root.resizable()
cv_width_size = 600
cv_height_size = 400

labelframe1 = tk.LabelFrame(root, text = 'parameters', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
labelframe1.place(width = 450, height = 250, x = 20, y = 10)
labelframe2 = tk.LabelFrame(root, text = 'plotting area', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
labelframe2.place(width = 500, height = 700, x = 480, y = 10)
labelframe3 = tk.LabelFrame(root, text = 'line information', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
labelframe3.place(width = 450, height = 400, x = 20, y = 250)

fitting_label = tk.Label(labelframe1, text = 'fitting method: ', font = ('Courier New', 11)).grid(row = 0, column = 0)
fitting_method = ['polynomial interpolation', 'gaussian interpolation',
                  'polynomial least square', 'polynomial ridge regression',
                  'neural network']
fitting_combobox = ttk.Combobox(labelframe1, font = ('Courier New', 11))
fitting_combobox['values'] = fitting_method
fitting_combobox.grid(row = 0, column = 1)
fitting_combobox.current(0)

parameterization_label = tk.Label(labelframe1, text = 'parameterization method: ', font = ('Courier New', 11)).grid(row = 1, column = 0)
parameterization_method = ['uniform parameterization', 'chordal parameterization', 
                           'centripetal parameterization', 'foley parameterization']
parameterization_combobox = ttk.Combobox(labelframe1, font = ('Courier New', 11))
parameterization_combobox['values'] = parameterization_method
parameterization_combobox.grid(row = 1, column = 1)
parameterization_combobox.current(0)

color_label = tk.Label(labelframe1, text = 'choose line color: ', font = ('Courier New', 11)).grid(row = 2, column = 0)
color_list = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 
                'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 
                'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 
                'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 
                'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 
                'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 
                'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 
                'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow', 'grey', 
                'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 
                'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 
                'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 
                'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 
                'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 
                'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 
                'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 
                'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 
                'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 
                'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 
                'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 
                'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
color_combobox = ttk.Combobox(labelframe1, font = ('Courier New', 11))
color_combobox['values'] = color_list
color_combobox.grid(row = 2, column = 1)
color_combobox.current(7)

sigma_label = tk.Label(labelframe1, text = 'sigma:', font = ('Courier New', 11)).grid(row = 3, column = 0)
sigma_text = tk.Text(labelframe1, width = 21, height = 1, font = ('Courier New', 11))
sigma_text.grid(row = 3, column = 1)
lambda_label = tk.Label(labelframe1, text = 'lambda:', font = ('Courier New', 11)).grid(row = 4, column = 0)
lambda_text = tk.Text(labelframe1, width = 21, height = 1, font = ('Courier New', 11))
lambda_text.grid(row = 4, column = 1)
degree_label = tk.Label(labelframe1, text = 'degree:', font = ('Courier New', 11)).grid(row = 5, column = 0)
degree_text = tk.Text(labelframe1, width = 21, height = 1, font = ('Courier New', 11))
degree_text.grid(row = 5, column = 1)

def plot():
    if sigma_text.get(1.0, "end-1c") == '':
        sigma = 1
    else:
        sigma = float(sigma_text.get(1.0, "end-1c"))
    if lambda_text.get(1.0, "end-1c") == '':
        lamda = 1
    else:
        lamda =  float(lambda_text.get(1.0, "end-1c"))
    if degree_text.get(1.0, "end-1c") == '':
        degree = 3
    else:
        degree =  int(degree_text.get(1.0, "end-1c"))
    
    result = do_curvefit(pos_x, pos_y, fitting_combobox.get(), parameterization_combobox.get(), sigma, lamda, degree)
    dict = {'fitting method': fitting_combobox.get(), 'parameterization method': parameterization_combobox.get(),
            'line color': color_combobox.get(), 'result': result}
    lines.append(dict)
    for line in lines:
        for i in range(np.size(line["result"], axis = 0) - 1):
            cv.create_line(line["result"][i, 0], line["result"][i, 1], line["result"][i+1, 0], line["result"][i+1, 1], fill = line["line color"], width = 2)
    for i in range(pos_x.size):
        cv.create_oval(pos_x[i] - 3, pos_y[i] - 3, pos_x[i] + 3, pos_y[i] + 3, fill = 'black')

    for item in line_treeview.get_children():
        line_treeview.delete(item)
    for i in range(len(lines)):
        line_treeview.insert('', i, values = (lines[i]["fitting method"], lines[i]["parameterization method"], lines[i]["line color"]))
plot_button = tk.Button(labelframe1, text='plot', font = ('Courier New', 11), command = plot)
plot_button.grid(row = 6, column = 0)

def clear():
    global pos_x, pos_y
    pos_x = np.array([])
    pos_y = np.array([])
    lines.clear()
    cv.delete("all")
    for item in line_treeview.get_children():
        line_treeview.delete(item)
clear_button = tk.Button(labelframe1, text='clear', font = ('Courier New', 11), command = clear)
clear_button.grid(row = 6, column = 1)
'''
def close():
    quit()
close_button = tk.Button(labelframe1, text='close', command = close)
close_button.grid(row = 2, column = 5)
'''
style = ttk.Style()
style.configure('Treeview.Heading', background = 'pink', font = ('Courier New', 11))
style.configure("Treeview", fieldbackground='gainsboro', foreground='black', font = ('Courier New', 8))
line_treeview = ttk.Treeview(labelframe3, show = 'headings', columns = ('fitting', 'parameterization', 'color'), height = 400)
line_treeview.column('fitting', width = 180, anchor = tk.CENTER)
line_treeview.column('parameterization', width = 180, anchor = tk.CENTER)
line_treeview.column('color', width = 80, anchor = tk.CENTER)
line_treeview.heading('fitting', text = 'fitting')
line_treeview.heading('parameterization', text = 'parameterization')
line_treeview.heading('color', text = 'color')
line_treeview.pack()

pos_x = np.array([])
pos_y = np.array([])
lines = []
cv = tk.Canvas(labelframe2, bg = 'white', width = 490, height = 607, background='whitesmoke')
moving_point = False
moving_index = -1
def on_button_release(event):
    global pos_x, pos_y, moving_point, moving_index
    if moving_point == False:
        pos_x = np.insert(pos_x, pos_x.size, event.x)
        pos_y = np.insert(pos_y, pos_y.size, event.y)
        lines.clear()
    else:
        pos_x[moving_index] = event.x
        pos_y[moving_index] = event.y
        lines.clear()
        moving_point = False
    cv.delete("all")
    for i in range(pos_x.size):
        cv.create_oval(pos_x[i] - 3, pos_y[i] - 3, pos_x[i] + 3, pos_y[i] + 3, fill = 'black')
cv.bind('<ButtonRelease-1>', on_button_release)

def on_button_press(event):
    global moving_point, moving_index
    dx = np.abs(event.x - pos_x)
    dy = np.abs(event.y - pos_y)
    for i in range(pos_x.size):
        if dx[i] < 20 and dy[i] < 20:
            moving_point = True
            moving_index = i
cv.bind('<Button-1>', on_button_press)

def on_mouse_move(event):
    if moving_point == True:
        cv.delete("all")

        for i in range(pos_x.size):
            if i == moving_index:
                cv.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill = 'black')
            else:
                cv.create_oval(pos_x[i] - 3, pos_y[i] - 3, pos_x[i] + 3, pos_y[i] + 3, fill = 'black')

cv.bind('<Motion>', on_mouse_move)

cv.pack()
root.mainloop()

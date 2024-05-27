import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from func_subdivision import do_chaikin2, do_chaikin3, do_interpolation

root = tk.Tk()
root.title('spline!!')
root.geometry('1000x700')

labelframe1 = tk.LabelFrame(root, text = 'parameters', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
labelframe1.place(width = 450, height = 250, x = 20, y = 10)
labelframe2 = tk.LabelFrame(root, text = 'plotting area', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
labelframe2.place(width = 500, height = 700, x = 480, y = 10)
#labelframe3 = tk.LabelFrame(root, text = 'line information', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
#labelframe3.place(width = 450, height = 400, x = 20, y = 250)

spline_label = tk.Label(labelframe1, text = 'Spline: ', font = ('Courier New', 11)).grid(row = 0, column = 0)
spline_method = ['subdivision curve']
spline_combobox = ttk.Combobox(labelframe1, font = ('Courier New', 11))
spline_combobox['values'] = spline_method
spline_combobox.grid(row = 0, column = 1)
spline_combobox.current(0)

subdivision_label = tk.Label(labelframe1, text = 'Subdivision method: ', font = ('Courier New', 11)).grid(row = 1, column = 0)
subdivision_method = ['Chaikin (2nd B-Spline)', 'Chaikin (3rd B-Spline)', 'interpolation']
subdivision_combobox = ttk.Combobox(labelframe1, font = ('Courier New', 11))
subdivision_combobox['values'] = subdivision_method
subdivision_combobox.grid(row = 1, column = 1)
subdivision_combobox.current(0)

class SubdivisionCurve:
    def __init__(self):
        self.pos_x = np.array([])
        self.pos_y = np.array([])
        self.counts = 0
        self.move_point = False
        self.move_index = -1

        self.new_x = 0
        self.new_y = 0
        self.plot()
# plot when combobox method change...
    def plot(self):  
        cv.delete("all")
        if self.counts > 2:
            self.new_x, self.new_y = self.pos_x, self.pos_y
            for i in range(5):
                if subdivision_combobox.get() == 'Chaikin (2nd B-Spline)':
                    self.new_x, self.new_y = do_chaikin2(self.new_x, self.new_y) 
                elif subdivision_combobox.get() == 'Chaikin (3rd B-Spline)':
                    self.new_x, self.new_y = do_chaikin3(self.new_x, self.new_y) 
                elif subdivision_combobox.get() == 'interpolation':
                    self.new_x, self.new_y = do_interpolation(self.new_x, self.new_y)
            for i in range(-1, self.new_x.size - 1):
                cv.create_line(self.new_x[i], self.new_y[i], self.new_x[i+1], self.new_y[i+1], fill = 'red')
            for i in range(-1, self.counts - 1):
                cv.create_line(self.pos_x[i], self.pos_y[i], self.pos_x[i+1], self.pos_y[i+1], fill = 'black')
        for i in range(self.counts):
            cv.create_oval(self.pos_x[i] - 3, self.pos_y[i] - 3, self.pos_x[i] + 3, self.pos_y[i] + 3, fill = 'black')
    def on_button_release(self, event):
        if self.move_point == False:
            self.pos_x = np.insert(self.pos_x, self.counts, event.x)
            self.pos_y = np.insert(self.pos_y, self.counts, event.y)
            self.counts += 1
        self.move_point = False
        self.plot()
    def on_button_press(self, event):
        dx = np.abs(event.x - self.pos_x)
        dy = np.abs(event.y - self.pos_y)
        for i in range(self.counts):
            if dx[i] < 10 and dy[i] < 10:
                self.move_point = True
                self.move_index = i
    def on_mouse_move(self, event):
        if self.move_point == True:
            self.pos_x[self.move_index] = event.x
            self.pos_y[self.move_index] = event.y
            self.plot()

cv = tk.Canvas(labelframe2, bg = 'white', width = 490, height = 607, background='whitesmoke')
line = SubdivisionCurve()
plot_button = tk.Button(labelframe1, text='plot', font = ('Courier New', 11), command = line.plot)
plot_button.grid(row = 6, column = 0)
clear_button = tk.Button(labelframe1, text='clear', font = ('Courier New', 11), command = line.__init__)
clear_button.grid(row = 6, column = 1)
cv.bind('<ButtonRelease-1>', line.on_button_release)
cv.bind('<Button-1>', line.on_button_press)
cv.bind('<Motion>', line.on_mouse_move)
def month_changed(event):
    line.plot
subdivision_combobox.bind('<<ComboboxSelected>>', month_changed)

cv.pack()
root.mainloop()
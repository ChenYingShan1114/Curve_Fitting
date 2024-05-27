import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from func_cubicspline import do_cubic_spline, cubic_spline_interpolation, tangent_to_ctrl, ctrl_to_tangent

root = tk.Tk()
root.title('spline!!')
root.geometry('800x700')

labelframe1 = tk.LabelFrame(root, text = 'parameters', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
labelframe1.place(width = 500, height = 130, x = 20, y = 10)
labelframe2 = tk.LabelFrame(root, text = 'plotting area', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
labelframe2.place(width = 750, height = 550, x = 20, y = 130)
#labelframe3 = tk.LabelFrame(root, text = 'information', font = ('Courier New', 20, 'bold'), borderwidth = 0, highlightthickness = 0)
#labelframe3.place(width = 370, height = 130, x = 400, y = 10)

spline_label = tk.Label(labelframe1, text = 'Spline: ', font = ('Courier New', 11)).grid(row = 0, column = 0)
spline_method = ['cubic spline']#, 'Bezier curve',
                  #'b-spline curve', 'subdivision curve']
spline_combobox = ttk.Combobox(labelframe1, font = ('Courier New', 11))
spline_combobox['values'] = spline_method
spline_combobox.grid(row = 0, column = 1)
spline_combobox.current(0)

continuity_label = tk.Label(labelframe1, text = 'Continuity condition: ', font = ('Courier New', 11)).grid(row = 1, column = 0)
continuity_method = ['C0 continuity', 'C1 continuity', 'G1 continuity', 'C2 continuity']
continuity_combobox = ttk.Combobox(labelframe1, font = ('Courier New', 11))
continuity_combobox['values'] = continuity_method
continuity_combobox.grid(row = 1, column = 1)
continuity_combobox.current(3)

class CubicSpline:
    def __init__(self):
        self.pos_x = np.array([])
        self.pos_y = np.array([])
        self.counts = 0
        self.move_point = False
        self.move_index = -1
        self.ctrl = False
        self.move_ctrl = False
        self.move_ctrl_left = False
        self.move_ctrl_right = False
        self.double_click = False

        self.t = 0
        self.xy = 0
        self.dxy_p = 0
        self.dxy_m = 0
        self.ddxy_p = 0
        self.ddxy_m = 0
        self.ctrl_left = 0
        self.ctrl_right = 0
        self.plot()

    def plot(self):
        cv.delete("all")
        if self.counts > 3:
            if continuity_combobox.get() == 'C2 continuity':
                self.t, self.xy, self.dxy_p, self.dxy_m, self.ddxy_p, self.ddxy_m = do_cubic_spline(self.pos_x, self.pos_y)      # calculate cubic spline
                self.ctrl_left, self.ctrl_right = tangent_to_ctrl(self.t, self.pos_x, self.pos_y, self.dxy_p, self.dxy_m)
            elif self.move_point == True or self.move_ctrl == True:
                self.dxy_p, self.dxy_m = ctrl_to_tangent(self.pos_x, self.pos_y, self.dxy_p, self.dxy_m, self.ctrl_left, self.ctrl_right)    # use arrow position to get tangent
                _, self.xy[:, 0] = cubic_spline_interpolation(self.t, self.pos_x, self.dxy_p[:, 0], self.dxy_m[:, 0], self.ddxy_p[:, 0], self.ddxy_m[:, 0])
                _, self.xy[:, 1] = cubic_spline_interpolation(self.t, self.pos_y, self.dxy_p[:, 1], self.dxy_m[:, 1], self.ddxy_p[:, 1], self.ddxy_m[:, 1])  
            if self.ctrl == True:
                for i in range(self.counts):
                    cv.create_rectangle(self.pos_x[i] - 5, self.pos_y[i] - 5, self.pos_x[i] + 5, self.pos_y[i] + 5, outline = 'black')
                    cv.create_line(self.ctrl_left[i, 0], self.ctrl_left[i, 1], self.pos_x[i], self.pos_y[i], fill = 'blue', arrow=tk.FIRST)
                    cv.create_line(self.ctrl_right[i, 0], self.ctrl_right[i, 1], self.pos_x[i], self.pos_y[i], fill = 'red', arrow=tk.FIRST)
            for i in range(np.size(self.xy, axis = 0) - 1):
                cv.create_line(self.xy[i, 0], self.xy[i, 1], self.xy[i+1, 0], self.xy[i+1, 1], fill = 'black', width = 2)
        for i in range(self.counts):
            cv.create_oval(self.pos_x[i] - 3, self.pos_y[i] - 3, self.pos_x[i] + 3, self.pos_y[i] + 3, fill = 'black')
    def reset(self):  
        continuity_combobox.current(3)
        self.plot()

    def on_button_release(self, event):
        if self.move_point == False and self.double_click == False and self.move_ctrl_left == False and self.move_ctrl_right == False and self.move_ctrl == False and self.ctrl == False:
            self.pos_x = np.insert(self.pos_x, self.counts, event.x)
            self.pos_y = np.insert(self.pos_y, self.counts, event.y)
            self.counts += 1
            continuity_combobox.current(3)
        self.move_point = False
        self.double_click = False
        self.move_ctrl_left = False
        self.move_ctrl_right = False
        self.move_ctrl = False
        self.plot()
    def on_button_press(self, event):
        dx = np.abs(event.x - self.pos_x)
        dy = np.abs(event.y - self.pos_y)
        for i in range(self.counts):
            if dx[i] < 10 and dy[i] < 10:
                self.move_point = True
                self.move_index = i
        if self.ctrl == True:
            dx_ctrl_left = np.abs(event.x - self.ctrl_left[:, 0])
            dy_ctrl_left = np.abs(event.y - self.ctrl_left[:, 1])
            dx_ctrl_right = np.abs(event.x- self.ctrl_right[:, 0])
            dy_ctrl_right = np.abs(event.y - self.ctrl_right[:, 1])
            for i in range(self.counts):
                if dx_ctrl_left[i] < 10 and dy_ctrl_left[i] < 10 and i != 0:
                    self.move_ctrl = True
                    self.move_ctrl_left = True
                    self.move_index = i
                elif dx_ctrl_right[i] < 10 and dy_ctrl_right[i] < 10 and i != self.counts - 1:
                    self.move_ctrl = True
                    self.move_ctrl_right = True
                    self.move_index = i
    def on_mouse_move(self, event):
        if self.move_point == True:
            self.ctrl_left[self.move_index, 0] = event.x + self.ctrl_left[self.move_index, 0] - self.pos_x[self.move_index]
            self.ctrl_right[self.move_index, 0] = event.x + self.ctrl_right[self.move_index, 0] - self.pos_x[self.move_index]
            self.ctrl_left[self.move_index, 1] = event.y + self.ctrl_left[self.move_index, 1] - self.pos_y[self.move_index]
            self.ctrl_right[self.move_index, 1] = event.y + self.ctrl_right[self.move_index, 1] - self.pos_y[self.move_index]    
            self.pos_x[self.move_index] = event.x
            self.pos_y[self.move_index] = event.y
            self.plot()

        if continuity_combobox.get() == 'C1 continuity':
            if self.move_ctrl_left == True:
                a = np.sqrt((self.ctrl_left[self.move_index, 0] - self.pos_x[self.move_index])**2 + (self.ctrl_left[self.move_index, 1] - self.pos_y[self.move_index])**2)
                b = np.sqrt((event.x - self.pos_x[self.move_index])**2 + (event.y - self.pos_y[self.move_index])**2)
                self.ctrl_right[self.move_index, 0] = self.pos_x[self.move_index] - (event.x - self.pos_x[self.move_index])# / b * a
                self.ctrl_right[self.move_index, 1] = self.pos_y[self.move_index] - (event.y - self.pos_y[self.move_index])# / b * a
                self.ctrl_left[self.move_index, 0] = self.pos_x[self.move_index] + (event.x - self.pos_x[self.move_index]) #/ b * a
                self.ctrl_left[self.move_index, 1] = self.pos_y[self.move_index] + (event.y - self.pos_y[self.move_index]) #/ b * a
                if self.move_index == self.counts - 1:
                    self.ctrl_right[self.move_index, 0] = self.pos_x[self.move_index]
                    self.ctrl_right[self.move_index, 1] = self.pos_y[self.move_index]
                self.plot()
            elif self.move_ctrl_right == True:
                a = np.sqrt((self.ctrl_right[self.move_index, 0] - self.pos_x[self.move_index])**2 + (self.ctrl_right[self.move_index, 1] - self.pos_y[self.move_index])**2)
                b = np.sqrt((event.x - self.pos_x[self.move_index])**2 + (event.y - self.pos_y[self.move_index])**2)
                self.ctrl_right[self.move_index, 0] = self.pos_x[self.move_index] + (event.x - self.pos_x[self.move_index]) #/ b * a
                self.ctrl_right[self.move_index, 1] = self.pos_y[self.move_index] + (event.y - self.pos_y[self.move_index]) #/ b * a
                self.ctrl_left[self.move_index, 0] = self.pos_x[self.move_index] - (event.x - self.pos_x[self.move_index]) #/ b * a
                self.ctrl_left[self.move_index, 1] = self.pos_y[self.move_index] - (event.y - self.pos_y[self.move_index]) #/ b * a
                if self.move_index == 0:
                    self.ctrl_left[self.move_index, 0] = self.pos_x[self.move_index]
                    self.ctrl_left[self.move_index, 1] = self.pos_y[self.move_index] 
                self.plot()  
        elif continuity_combobox.get() == 'G1 continuity':
            if self.move_ctrl_left == True:
                a = np.sqrt((self.ctrl_right[self.move_index, 0] - self.pos_x[self.move_index])**2 + (self.ctrl_right[self.move_index, 1] - self.pos_y[self.move_index])**2)
                b = np.sqrt((event.x - self.pos_x[self.move_index])**2 + (event.y - self.pos_y[self.move_index])**2)
                self.ctrl_right[self.move_index, 0] = self.pos_x[self.move_index] - (event.x - self.pos_x[self.move_index]) / b * a
                self.ctrl_right[self.move_index, 1] = self.pos_y[self.move_index] - (event.y - self.pos_y[self.move_index]) / b * a
                self.ctrl_left[self.move_index, 0] = self.pos_x[self.move_index] + (event.x - self.pos_x[self.move_index])
                self.ctrl_left[self.move_index, 1] = self.pos_y[self.move_index] + (event.y - self.pos_y[self.move_index])
                if self.move_index == self.counts - 1:
                    self.ctrl_right[self.move_index, 0] = self.pos_x[self.move_index]
                    self.ctrl_right[self.move_index, 1] = self.pos_y[self.move_index]
                self.plot()
            elif self.move_ctrl_right == True:
                a = np.sqrt((self.ctrl_left[self.move_index, 0] - self.pos_x[self.move_index])**2 + (self.ctrl_left[self.move_index, 1] - self.pos_y[self.move_index])**2)
                b = np.sqrt((event.x - self.pos_x[self.move_index])**2 + (event.y - self.pos_y[self.move_index])**2)
                self.ctrl_right[self.move_index, 0] = self.pos_x[self.move_index] + (event.x - self.pos_x[self.move_index])
                self.ctrl_right[self.move_index, 1] = self.pos_y[self.move_index] + (event.y - self.pos_y[self.move_index])
                self.ctrl_left[self.move_index, 0] = self.pos_x[self.move_index] - (event.x - self.pos_x[self.move_index]) / b * a
                self.ctrl_left[self.move_index, 1] = self.pos_y[self.move_index] - (event.y - self.pos_y[self.move_index]) / b * a
                if self.move_index == 0:
                    self.ctrl_left[self.move_index, 0] = self.pos_x[self.move_index]
                    self.ctrl_left[self.move_index, 1] = self.pos_y[self.move_index] 
                self.plot()
        elif continuity_combobox.get() == 'C0 continuity':
            if self.move_ctrl_left == True:
                self.ctrl_left[self.move_index, 0] = event.x
                self.ctrl_left[self.move_index, 1] = event.y
                if self.move_index == self.counts - 1:
                    self.ctrl_right[self.move_index, 0] = self.pos_x[self.move_index]
                    self.ctrl_right[self.move_index, 1] = self.pos_y[self.move_index]
                self.plot()
            elif self.move_ctrl_right == True:
                self.ctrl_right[self.move_index, 0] = event.x
                self.ctrl_right[self.move_index, 1] = event.y
                if self.move_index == 0:
                    self.ctrl_left[self.move_index, 0] = self.pos_x[self.move_index]
                    self.ctrl_left[self.move_index, 1] = self.pos_y[self.move_index] 
                self.plot()    
    def double_button(self, event):
        self.double_click = True
        if self.ctrl == False and self.counts > 3:
            self.ctrl = True
        else:
            self.ctrl = False

cv = tk.Canvas(labelframe2, bg = 'white', width = 750, height = 550, background='whitesmoke')
line = CubicSpline()
reset_button = tk.Button(labelframe1, text='reset', font = ('Courier New', 11), command = line.reset)
reset_button.grid(row = 6, column = 0)
clear_button = tk.Button(labelframe1, text='clear', font = ('Courier New', 11), command = line.__init__)
clear_button.grid(row = 6, column = 1)
cv.bind('<ButtonRelease-1>', line.on_button_release)
cv.bind('<Button-1>', line.on_button_press)
cv.bind('<Motion>', line.on_mouse_move)
cv.bind('<Double-Button-1>', line.double_button)

cv.pack()
root.mainloop()




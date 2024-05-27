import numpy as np

def do_chaikin2(x, y):
    xx = np.zeros(2 * x.size)
    yy = np.zeros(2 * y.size)
    for i in range(-1, x.size-1):
        xx[2*i] = 0.25 * x[i-1] + 0.75 * x[i]
        xx[2*i+1] = 0.75 * x[i] + 0.25 * x[i+1]
        yy[2*i] = 0.25 * y[i-1] + 0.75 * y[i]
        yy[2*i+1] = 0.75 * y[i] + 0.25 * y[i+1]
    return xx, yy

def do_chaikin3(x, y):
    xx = np.zeros(2 * x.size)
    yy = np.zeros(2 * y.size)
    for i in range(-1, x.size-1):
        xx[2*i] = 0.125 * x[i-1] + 0.75 * x[i] + 0.125 * x[i+1]
        xx[2*i+1] = 0.5 * x[i] + 0.5 * x[i+1]
        yy[2*i] = 0.125 * y[i-1] + 0.75 * y[i] + 0.125 * y[i+1]
        yy[2*i+1] = 0.5 * y[i] + 0.5 * y[i+1]
    return xx, yy

def do_interpolation(x, y):
    xx = np.zeros(2 * x.size)
    yy = np.zeros(2 * y.size)
    for i in range(-2, x.size-2):
        alpha = 0.1
        xx[2*i] = x[i]
        xx[2*i+1] = 0.5 * (x[i] + x[i+1]) + alpha * 0.5 * (x[i] + x[i+1] - x[i-1] - x[i+2])
        yy[2*i] = y[i]
        yy[2*i+1] = 0.5 * (y[i] + y[i+1]) + alpha * 0.5 * (y[i] + y[i+1] - y[i-1] - y[i+2])
    return xx, yy

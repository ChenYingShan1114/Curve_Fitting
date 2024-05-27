import numpy as np
from numpy.linalg import inv
from func_parameterization import parameterization

def do_cubic_spline(pos_x, pos_y):
    t, _ = parameterization(pos_x, pos_y, 'chordal')
    dx_p, dx_m, ddx_p, ddx_m = cubic_spline(t, pos_x)
    _, xx = cubic_spline_interpolation(t, pos_x, dx_p, dx_m, ddx_p, ddx_m)
    dy_p, dy_m, ddy_p, ddy_m = cubic_spline(t, pos_y)
    _, yy = cubic_spline_interpolation(t, pos_y, dy_p, dy_m, ddy_p, ddy_m)
    return t, np.array([xx, yy]).T, np.array([dx_p, dy_p]).T, np.array([dx_m, dy_m]).T, np.array([ddx_p, ddy_p]).T, np.array([ddx_m, ddy_m]).T

# cubic_spline: t, pos_x -> dxy, ddxy
def cubic_spline(data_x, data_y):
    H = np.zeros(data_x.size - 1)
    for i in range(H.size):
        H[i] = data_x[i+1] - data_x[i]
    X = np.zeros([data_x.size - 2, data_x.size - 2])
    Y = np.zeros(data_x.size - 2)
    for i in range(np.size(X, axis = 0)):
        Y[i] = 6 / H[i+1] * (data_y[i+2] - data_y[i+1]) - 6 / H[i] * (data_y[i+1] - data_y[i])
        if i == 0:
            X[i, i] = 2 * (H[i+1] + H[i])
            X[i, i+1] = H[i+1]
        elif i == np.size(X, axis = 0) - 1:
            X[i, i-1] = H[i]
            X[i, i] = 2 * (H[i+1] + H[i])
        else:
            X[i, i-1] = H[i]
            X[i, i] = 2 * (H[i+1] + H[i])
            X[i, i+1] = H[i+1]
    curvature = np.zeros(data_x.size)
    curvature[1:-1] = np.dot(inv(X), Y)

    tangent = np.zeros(data_x.size)
    for i in range(data_x.size-1):
        C = (data_y[i] - curvature[i] / 6 * H[i] * H[i]) / H[i]
        D = (data_y[i+1] - curvature[i+1] / 6 * H[i] * H[i]) / H[i]
        tangent[i] = -curvature[i] / 2 * H[i] - C + D
    tangent[-1] = -curvature[-1] / 2 * H[-1] - C + D
    return tangent, tangent, curvature, curvature

# cubic_spline_interpolation: t, pos_x, pox_y, dxy, ddxy -> xy
def cubic_spline_interpolation(t, pos_x, dx_p, dx_m, ddx_p, ddx_m):
    inter_num = 30
    tt = np.zeros(inter_num * (t.size - 1) + 1)
    xx = np.zeros(inter_num * (t.size - 1) + 1)
    for i in range(t.size - 1):
        A = np.zeros([4, 4])
        A[0, :] = [1, t[i], t[i]**2, t[i]**3]
        A[1, :] = [1, t[i+1], t[i+1]**2, t[i+1]**3]
        A[2, :] = [0, 1, 2 * t[i], 3 * t[i]**2]
        A[3, :] = [0, 1, 2 * t[i+1], 3 * t[i+1]**2]
        B = np.array([pos_x[i], pos_x[i+1], dx_p[i], dx_m[i+1]])
        C = np.dot(inv(A), B)
        for j in range(inter_num):
            tmp_t = t[i] + (t[i+1] - t[i]) / inter_num * j
            tt[inter_num*i+j] = tmp_t
            xx[inter_num*i+j] = C[0] + C[1] * tmp_t + C[2] * tmp_t**2 + C[3] * tmp_t**3
    tt[-1] = t[-1]
    xx[-1] = C[0] + C[1] * t[-1] + C[2] * t[-1]**2 + C[3] * t[-1]**3
    return tt, xx

def tangent_to_ctrl(t, pos_x, pos_y, tangent_p, tangent_m):
    left = np.zeros([pos_x.size, 2])
    right = np.zeros([pos_x.size, 2])
    left[0, 0] = pos_x[0]
    left[0, 1] = pos_y[0]
    right[-1, 0] = pos_x[-1]
    right[-1, 1] = pos_y[-1]
    for i in range(1, pos_x.size):
        left[i, 0] = -tangent_m[i, 0] * 0.1 + pos_x[i]
        left[i, 1] = -tangent_m[i, 1] * 0.1 + pos_y[i]
    for i in range(0, pos_x.size - 1):
        right[i, 0] = tangent_p[i, 0] * 0.1 + pos_x[i]
        right[i, 1] = tangent_p[i, 1] * 0.1 + pos_y[i]
    return left, right

def ctrl_to_tangent(pos_x, pos_y, tangent_p, tangent_m, ctrl_left, ctrl_right):
    for i in range(1, pos_x.size):
        tangent_m[i, 0] = -10 * (ctrl_left[i, 0] - pos_x[i])
        tangent_m[i, 1] = -10 * (ctrl_left[i, 1] - pos_y[i])
    for i in range(0, pos_x.size-1):
        tangent_p[i, 0] = 10 * (ctrl_right[i, 0] - pos_x[i])
        tangent_p[i, 1] = 10 * (ctrl_right[i, 1] - pos_y[i])
    return tangent_p, tangent_m
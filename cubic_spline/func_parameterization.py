import numpy as np

def uniform_para(pos_x, pos_y):
    t = np.linspace(0, 1, pos_x.size)
    return t
def chordal_para(pos_x, pos_y):
    h = np.zeros(pos_x.size - 1)
    for i in range(h.size):
        h[i] = np.sqrt((pos_x[i+1] - pos_x[i])**2 + (pos_y[i+1] - pos_y[i])**2)
    t = np.zeros(pos_x.size)
    for i in range(1, t.size):
        t[i] = t[i-1] + h[i-1] / np.sum(h)
    return t
def centripetal_para(pos_x, pos_y):
    h = np.zeros(pos_x.size - 1)
    for i in range(h.size):
        h[i] = np.sqrt(np.sqrt((pos_x[i+1] - pos_x[i])**2 + (pos_y[i+1] - pos_y[i])**2))
    t = np.zeros(pos_x.size)
    for i in range(1, t.size):
        t[i] = t[i-1] + h[i-1] / np.sum(h)
    return t
#https://www.researchgate.net/profile/Gregory-Nielson-2/publication/308994559_1989_Knot_Selection_FoleyNielson/links/57fd281808ae6750f8065be3/1989-Knot-Selection-Foley-Nielson.pdf
def d(index1, index2, pos_x, pos_y):
    var_xy = np.average((pos_x - np.average(pos_x)) * (pos_y - np.average(pos_y)))
    g = np.var(pos_x) * np.var(pos_y) - var_xy**2
    Q = np.array([[np.var(pos_y), -var_xy], [-var_xy, np.var(pos_x)]]) / g
    a = pos_x[index1] - pos_x[index2]
    b = pos_y[index1] - pos_y[index2]
    return np.sqrt(a * (a * Q[0, 0] + b * Q[1, 0]) + b * (a * Q[0, 1] + b * Q[1, 1]))
def foley_para(pos_x, pos_y):
    theta = np.zeros(pos_x.size - 1)
    for i in range(1, pos_x.size - 1):
        d1 = d(i-1, i, pos_x, pos_y)
        d2 = d(i, i+1, pos_x, pos_y)
        d3 = d(i-1, i+1, pos_x, pos_y)
        theta[i] = np.pi - np.arccos((d1**2 + d2**2 - d3**2) / 2 / d1 / d2)
        theta[i] = np.min([theta[i], np.pi / 2])
    h = np.zeros(pos_x.size - 1)
    for i in range(pos_x.size - 1):
        if i == 0:
            d2 = d(i, i+1, pos_x, pos_y)
            d3 = d(i+1, i+2, pos_x, pos_y)
            h[i] = d2 * (1 + 1.5 * theta[i+1] * d3 / (d2 + d3))
        if i == pos_x.size - 2:
            d1 = d(i-1, i, pos_x, pos_y)
            d2 = d(i, i+1, pos_x, pos_y)
            h[i] = d2 * (1 + 1.5 * theta[i] * d1 / (d1 + d2))
        else:
            d1 = d(i-1, i, pos_x, pos_y)
            d2 = d(i, i+1, pos_x, pos_y)
            d3 = d(i+1, i+2, pos_x, pos_y)
            h[i] = d2 * (1 + 1.5 * theta[i] * d1 / (d1 + d2) + 1.5 * theta[i+1] * d3 / (d2 + d3))
    t = np.zeros(pos_x.size)
    for i in range(1, t.size):
        t[i] = t[i-1] + h[i-1] / np.sum(h)
    return t   

def parameterization(pos_x, pos_y, para_way):
    if pos_x.size == 2:
        t = np.linspace(0, 1, 2)
    else:
        if para_way == 'uniform':
            t = uniform_para(pos_x, pos_y)
        elif para_way == 'chordal':
            t = chordal_para(pos_x, pos_y)
        elif para_way == 'centripetal':
            t = centripetal_para(pos_x, pos_y)
        elif para_way == 'foley':
            t = foley_para(pos_x, pos_y)
        else:
            print('func_paramatrix.py: please choose correct parameterization method.')
            quit()
    tt = np.linspace(t[0], t[-1], 10 * t.size)
    return t, tt
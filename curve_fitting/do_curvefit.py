import numpy as np
from func_parameterization import parameterization
from func_fitting import poly_inv, gauss_inv, poly_lsq, nn

def do_curvefit(pos_x, pos_y, fit_way, para_way, sigma, lamda, degree):
    if para_way == 'uniform parameterization':
        t, tt = parameterization(pos_x, pos_y, 'uniform')
    elif para_way == 'chordal parameterization':
        t, tt = parameterization(pos_x, pos_y, 'chordal')
    elif para_way == 'centripetal parameterization':
        t, tt = parameterization(pos_x, pos_y, 'centripetal')
    elif para_way == 'foley parameterization':
        t, tt = parameterization(pos_x, pos_y, 'foley')
    
    if fit_way == 'polynomial interpolation':
        return poly_inv(t, tt, pos_x, pos_y)
    elif fit_way == 'gaussian interpolation':
        return gauss_inv(t, tt, pos_x, pos_y, sigma = sigma)        
    elif fit_way == 'polynomial least square':
        return poly_lsq(t, tt, pos_x, pos_y, degree = degree)
    elif fit_way == 'polynomial ridge regression':
        return poly_lsq(t, tt, pos_x, pos_y, degree = degree, lamda = lamda)
    elif fit_way == 'neural network':
        return np.array([nn(t, pos_x, tt)[:, 0], nn(t, pos_y, tt)[:, 0]]).T
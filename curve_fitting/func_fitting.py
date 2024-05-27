import numpy as np
from numpy.linalg import inv
import tensorflow as tf

def poly_inv(para, para_fit, data_x, data_y = np.array([]), data_z = np.array([])):
    A = np.vander(para, para.size, increasing = True)
    if data_y.size == 0:
        B = data_x
    elif data_z.size == 0:
        B = np.zeros([data_x.size, 2])
        B[:, 0] = data_x
        B[:, 1] = data_y
    else:
        B = np.zeros([data_x.size, 3])
        B[:, 0] = data_x
        B[:, 1] = data_y
        B[:, 2] = data_z
    alpha = np.dot(inv(A), B)
    AA = np.vander(para_fit, np.size(alpha, axis = 0), increasing = True)
    BB = np.dot(AA, alpha)
    return BB
def gaussian(x, xi, sigma):
    return np.exp(-(x - xi)**2 / (2 * sigma**2)) / np.sqrt(2 * np.pi)
def gauss_inv(para, para_fit, data_x, data_y = np.array([]), data_z = np.array([]), sigma = 1):
    A = np.ones([para.size + 1, para.size + 1])
    for i in range(np.size(A, axis = 0) - 1):
        for j in range(1, np.size(A, axis = 1)):
            A[i, j] = gaussian(para[j-1], para[i], sigma)
    for j in range(1, np.size(A, axis = 1)):
        A[-1, j] = gaussian(para[j-1], 0.5 * (para[-2] + para[-1]), sigma) 
    if data_y.size == 0:
        B = np.insert(data_x, data_x.size, 0.5 * (data_x[-2] + data_x[-1]))
    elif data_z.size == 0:
        B = np.zeros([data_x.size + 1, 2])
        B[:, 0] = np.insert(data_x, data_x.size, 0.5 * (data_x[-2] + data_x[-1]))
        B[:, 1] = np.insert(data_y, data_y.size, 0.5 * (data_y[-2] + data_y[-1]))
    else:
        B = np.zeros([data_x.size + 1, 3])
        B[:, 0] = np.insert(data_x, data_x.size, 0.5 * (data_x[-2] + data_x[-1]))
        B[:, 1] = np.insert(data_y, data_y.size, 0.5 * (data_y[-2] + data_y[-1]))
        B[:, 2] = np.insert(data_z, data_z.size, 0.5 * (data_z[-2] + data_z[-1]))
    b = np.dot(inv(A), B)
    AA = np.ones([para_fit.size, np.size(b, axis = 0)])
    for i in range(np.size(AA, axis = 0)):
        for j in range(1, np.size(AA, axis = 1)):
            AA[i, j] = gaussian(para[j-1], para_fit[i], sigma)
    BB = np.dot(AA, b)
    return BB   
def poly_lsq(para, para_fit, data_x, data_y = np.array([]), data_z = np.array([]), degree = 1, lamda = 0):
    if para.size < degree + 1:
        print('overfit')
    A = np.vander(para, degree + 1, increasing = True)  
    if data_y.size == 0:
        B = data_x
    elif data_z.size == 0:
        B = np.zeros([data_x.size, 2])
        B[:, 0] = data_x
        B[:, 1] = data_y
    else:
        B = np.zeros([data_x.size, 3])
        B[:, 0] = data_x
        B[:, 1] = data_y
        B[:, 2] = data_z
    L = lamda * np.identity(np.size(A, axis = 1))
    theta = np.dot(np.dot(inv(np.dot(A.T, A) + L), A.T), B)
    AA = np.vander(para_fit, degree + 1, increasing = True)
    BB = np.dot(AA, theta)
    return BB
def nn(para, data_x, para_fit):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units = 1, input_shape=([1]), activation = 'linear'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(units = 164, activation = 'relu'),
        tf.keras.layers.Dense(1)               
    ])
    model.compile(optimizer="adam", loss='mse')
    model.fit(para, data_x, epochs = 100)
    return model.predict(para_fit)

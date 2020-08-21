# coding:utf-8
# 【谷雨课堂】干货实战 No.021 隐藏在数学背后的神秘图像
# 作者：谷雨
# 牛顿分形

import numpy as np
import matplotlib.pyplot as plt
from numba import jit


# 函数
@jit('complex64(complex64)', nopython=True)
def f(z):
    return z*z*z - 1


# 导数
@jit('complex64(complex64)', nopython=True)
def df(z):
    return 3*z*z


# 迭代器
@jit('float64(complex64)', nopython=True)
def iterate(z):
    num = 0
    while abs(f(z)) > 1e-4:
        w = z - f(z)/df(z)
        num += np.exp(-1/abs(w-z))
        z = w
    return num


# 画牛顿环
def draw(imgsize=600):
    y, x = np.ogrid[1: -1: imgsize*2j, -1: 1: imgsize*2j]
    z = x + y*1j
    img = np.frompyfunc(iterate, 1, 1)(z).astype(np.float)
    fig = plt.figure(figsize=(imgsize/100.0, imgsize/100.0), dpi=100)
    axi = fig.add_axes([0, 0, 1, 1], aspect=1)
    axi.axis('off')
    axi.imshow(img, cmap='hot')
    fig.savefig('newton.png')
    plt.show()
    
draw()
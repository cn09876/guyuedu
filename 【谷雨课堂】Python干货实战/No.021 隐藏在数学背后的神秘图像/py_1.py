# coding:utf-8
# 【谷雨课堂】干货实战 No.021 隐藏在数学背后的神秘图像
# 作者：谷雨
# 朱利亚分形

import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from PIL import Image

MAXITERS = 500
RADIUS = 4
CONST = 0.7


@jit('float32(complex64)')
def escape(z):
    for i in range(MAXITERS):
        if z.real * z.real + z.imag * z.imag > RADIUS:
            break
        z = (z*z + CONST) / (z*z - CONST)
    return i


def main(xmin, xmax, ymin, ymax, width, height):
    y, x = np.ogrid[ymax: ymin: height*2j, xmin: xmax: width*2j]
    z = x + y*1j
    img = np.asarray(np.frompyfunc(escape, 1, 1)(z)).astype(np.float)
    img /= np.max(img)
    img = np.sin(img**2 * np.pi)**0.8 
    fig = plt.figure(figsize=(width/100.0, height/100.0), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], aspect=1)
    ax.axis('off')
    ax.imshow(img, cmap='hot')
    #fig.savefig('julia.png')
    plt.show()
    


main(-2, 2, -1.6, 1.6, 1200, 1000)
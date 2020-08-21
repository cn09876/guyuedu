# coding:utf-8
# 【谷雨课堂】干货实战 No.021 隐藏在数学背后的神秘图像
# 作者：谷雨
# 曼德布洛特(Mandelbrot)集合

import pygame
width, height = 1300,1000
screen = pygame.display.set_mode((width, height))
xaxis = width / 2.2 + 60
yaxis = height / 2
scale = 300
maxit = 200
for ty in range(501):
    for tx in range(width):
        d = 0 + 0j
        c = complex(float(tx - xaxis) / scale, float(ty - yaxis) / scale)

        for linux in range(maxit):
            d = d*d + c
            if abs(d) > 2:
                col=(linux % 32 * 8, linux % 16 * 16, linux % 8 * 32)
                break
        else:
            col = (255, 0, 255)

        screen.set_at((tx, ty), col)
        screen.set_at((tx, height-ty), col)
    pygame.display.update()
input("Done")
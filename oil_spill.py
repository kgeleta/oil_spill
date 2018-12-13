from pylab import *
from matplotlib import colors
import matplotlib.pyplot as plt


n = 11
m = 0.098
d = 0.18
Cmax = -100
P = 0.18
wind = [0, 0, 0, 0]
cmap = colors.ListedColormap(['green', 'blue', 'black'])
bounds = [-200, -1, 1, 2000]
norm = colors.BoundaryNorm(bounds, cmap.N)


def initialize():
    global layer1, next_layer1
    layer1 = zeros([n, n])
    for x in range(n):
        for y in range(n):
            if x == 0 or x == 10 or y == 0 or y == 10:
                layer1[x, y] = -1
            if x == 5 and y == 5:
                layer1[x, y] = 1000
    next_layer1 = zeros([n, n])


def observe():
    global layer1, next_layer1
    fig, ax = plt.subplots()
    ax.imshow(layer1, vmin=0, vmax=1, cmap=cmap, norm=norm)
    plt.show()


def update():
    global layer1, next_layer1
    next_layer1 = layer1
    for x in range(1, n-1):
        for y in range(1, n-1):
            if layer1[x, y] >= 0:
                next_layer1[x, y] = layer1[x, y]
                if layer1[x-1, y-1] >= 0:
                    next_layer1[x, y] += m*d*(layer1[x-1, y-1] - layer1[x, y])
                if layer1[x, y-1] >= 0:
                    next_layer1[x, y] += m*(layer1[x, y-1] - layer1[x, y])
                if layer1[x+1, y-1] >= 0:
                    next_layer1[x, y] += m*d*(layer1[x+1, y-1] - layer1[x, y])
                if layer1[x+1, y] >= 0:
                    next_layer1[x, y] += m*(layer1[x+1, y] - layer1[x, y])
                if layer1[x+1, y+1] >= 0:
                    next_layer1[x, y] += m*d*(layer1[x+1, y+1] - layer1[x, y])
                if layer1[x, y+1] >= 0:
                    next_layer1[x, y] += m*(layer1[x, y+1] - layer1[x, y])
                if layer1[x-1, y+1] >= 0:
                    next_layer1[x, y] += m*d*(layer1[x-1, y+1] - layer1[x, y])
                if layer1[x-1, y] >= 0:
                    next_layer1[x, y] += m*(layer1[x-1, y] - layer1[x, y])

                if Cmax < layer1[x-1, y-1] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
                if Cmax < layer1[x, y-1] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
                if Cmax < layer1[x+1, y-1] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
                if Cmax < layer1[x+1, y] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
                if Cmax < layer1[x+1, y+1] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
                if Cmax < layer1[x, y+1] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
                if Cmax < layer1[x-1, y+1] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
                if Cmax < layer1[x-1, y] < 0:
                    next_layer1[x, y] -= P * next_layer1[x, y]
            if layer1[x, y] < 0:
                next_layer1[x, y] = layer1[x, y]

    next_layer1, layer1 = layer1, next_layer1


initialize()

for t in range(7):
    observe()
    update()
#observe()
#update()
#observe()

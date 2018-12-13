from pylab import *
import matplotlib.pyplot as plt


n = 100
p = 0.5
T = 4


def initialize():
    global config, nextconfig
    config = zeros([n,n])
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random() < p else 0
    nextconfig = zeros([n, n])


def observe():
    global config, nextconfig
    fig, ax = plt.subplots()
    im = ax.imshow(config, vmin=0, vmax=1, cmap=cm.binary)
    plt.show()


def update():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += config[(x + dx)%n, (y + dy)%n]
            nextconfig[x, y] = 1 if count >= 4 else 0
    config, nextconfig = nextconfig, config


initialize()
for t in range(T):
    observe()
    update()




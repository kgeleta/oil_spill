from pylab import *
from matplotlib import colors
from pprint import pprint
import matplotlib.pyplot as plt


n = 100
# Spreading without wind and current:
m = 0.098
d = 0.18
# Shoreline deposition:
C_max = 7
P = 0.18
# Wind and current:
R_w = 0.09  # 0.03 to 0.16
wind_max = 10
current_max = 2
# directions:
NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3

cmap = colors.ListedColormap(['green', 'blue', 'black'])
bounds = [(-250), (-1), 1, 2000]
norm = colors.BoundaryNorm(bounds, cmap.N)


class Cell:
    def __init__(self, mass, land, wind, current):
        self.mass = mass
        self.land = land
        self.wind = wind
        self.current = current

    def __repr__(self):
        if self.land:
            return "X%.1fX" % self.mass
        else:
            return "%.1f" % self.mass


def initialize():
    # todo: refactor names
    global test, next_test
    test = [[Cell(0, False, [0, 0, 0, 0], [0, 0, 0, 0]) for j in range(n)] for i in range(n)]
    next_test = [[Cell(0, False, [0, 0, 0, 0], [0, 0, 0, 0]) for j in range(n)] for i in range(n)]
    for x in range(n):
        for y in range(n):
            if 47 < x < 53 and 45 < y < 53:
                test[x][y].land = True
            if 48 < x < 52 and y > 30:
                test[x][y].wind = [0, 0, 0, 10]
                test[x][y].current = [0, 0, 0, 2.5]
            if 45 < x < 55 and 25 < y < 35:
                test[x][y].mass = 99


def update():
    global test, next_test
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0 or i == n-1 or j == n-1:
                next_test[i][j].mass = test[i][j].mass
                next_test[i][j].land = test[i][j].land
                next_test[i][j].wind = test[i][j].wind
                next_test[i][j].current = test[i][j].current
            else:
                if test[i][j].land:
                    # skpiuj wartosci z poprzedniej iteracji
                    next_test[i][j].mass = test[i][j].mass
                    next_test[i][j].land = test[i][j].land
                    next_test[i][j].wind = test[i][j].wind
                    next_test[i][j].current = test[i][j].current
                if not test[i][j].land:
                    # skopiuj wartosci z poprzedniej iteracji
                    next_test[i][j].mass = test[i][j].mass
                    next_test[i][j].land = test[i][j].land
                    next_test[i][j].wind = test[i][j].wind
                    next_test[i][j].current = test[i][j].current

                    # if neighbor is not a land:
                    # cardinal directions:
                    if not test[i-1][j].land:
                        w = ((test[i][j].current[WEST] + test[i-1][j].current[WEST])/2/current_max) +\
                            R_w * ((test[i][j].wind[WEST] + test[i-1][j].wind[WEST])/2/wind_max)
                        next_test[i][j].mass += m*((1+w)*test[i-1][j].mass - (1-w)*test[i][j].mass)
                    if not test[i+1][j].land:
                        e = ((test[i][j].current[EAST] + test[i+1][j].current[EAST])/2/current_max) +\
                            R_w * ((test[i][j].wind[EAST] + test[i+1][j].wind[EAST])/2/wind_max)
                        next_test[i][j].mass += m*((1+e)*test[i+1][j].mass - (1-e)*test[i][j].mass)
                    if not test[i][j-1].land:
                        s = ((test[i][j].current[SOUTH] + test[i][j-1].current[SOUTH])/2/current_max) +\
                            R_w * ((test[i][j].wind[SOUTH] + test[i][j-1].wind[SOUTH])/2/wind_max)
                        next_test[i][j].mass += m*((1+s)*test[i][j-1].mass - (1-s)*test[i][j].mass)
                    if not test[i][j+1].land:
                        # todo: wind + current:
                        next_test[i][j].mass += m*(test[i][j+1].mass - test[i][j].mass)

                    # intermediate directions:
                    if not test[i-1][j-1].land:
                        next_test[i][j].mass += m*d*(test[i-1][j-1].mass - test[i][j].mass)
                    if not test[i-1][j+1].land:
                        next_test[i][j].mass += m*d*(test[i-1][j+1].mass - test[i][j].mass)
                    if not test[i+1][j-1].land:
                        next_test[i][j].mass += m*d*(test[i+1][j-1].mass - test[i][j].mass)
                    if not test[i+1][j+1].land:
                        next_test[i][j].mass += m*d*(test[i+1][j+1].mass - test[i][j].mass)

    # druga petla - osadzanie na brzegu bierze wartosci z next_test wiec musi byc juz cala gotowa
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0 or i == n-1 or j == n-1:
                None
            else:
                if not test[i][j].land:
                    # jesli sasiad jest ladem i masa na tym ladzie mniejsza od max - czesc masy osadza sie na ladzie
                    if next_test[i - 1][j].land and next_test[i - 1][j].mass <= C_max:
                        next_test[i - 1][j].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass
                    if next_test[i + 1][j].land and next_test[i + 1][j].mass <= C_max:
                        next_test[i + 1][j].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass
                    if next_test[i][j - 1].land and next_test[i][j - 1].mass <= C_max:
                        next_test[i][j - 1].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass
                    if next_test[i][j + 1].land and next_test[i][j + 1].mass <= C_max:
                        next_test[i][j + 1].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass

                    if next_test[i - 1][j - 1].land and next_test[i - 1][j - 1].mass <= C_max:
                        next_test[i - 1][j - 1].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass
                    if next_test[i - 1][j + 1].land and next_test[i - 1][j + 1].mass <= C_max:
                        next_test[i - 1][j + 1].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass
                    if next_test[i + 1][j - 1].land and next_test[i + 1][j - 1].mass <= C_max:
                        next_test[i + 1][j - 1].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass
                    if next_test[i + 1][j + 1].land and next_test[i + 1][j + 1].mass <= C_max:
                        next_test[i + 1][j + 1].mass += P * next_test[i][j].mass
                        next_test[i][j].mass -= P * next_test[i][j].mass
    test, next_test = next_test, test


def to_matrix():
    global test, next_test
    mass_matrix = zeros([n, n])
    for i in range(n):
        for j in range(n):
            if test[i][j].land:
                mass_matrix[i, j] = (-200)
            if not test[i][j].land:
                mass_matrix[i, j] = test[i][j].mass
    if mass_matrix[10, 10] < 0:
        print("ALERT")
    return mass_matrix


def observe():
    global test, next_test
    fig, ax = plt.subplots()
    mm = to_matrix()
    ax.imshow(mm, vmin=0, vmax=1, cmap=cmap, norm=norm)
    plt.show()


initialize()

for t in range(100):
    if t % 20 == 0:
        observe()
    update()

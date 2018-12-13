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
    global surface_layer, next_surface_layer
    surface_layer = [[Cell(0, False, [10, 0, 0, 0], [0, 0, 0, 0]) for j in range(n)] for i in range(n)]
    next_surface_layer = [[Cell(0, False, [10, 0, 0, 0], [0, 0, 0, 0]) for j in range(n)] for i in range(n)]
    for x in range(n):
        for y in range(n):
            if 35 < x < 40 and 35 < y < 40:
                surface_layer[x][y].land = True
            if x < 45:
                surface_layer[x][y].wind = [0, 0, 0, 0]
                surface_layer[x][y].current = [0, 0, 1.5, 0]
            if 45 < x < 55 and 25 < y < 35:
                surface_layer[x][y].mass = 99


def update():
    global surface_layer, next_surface_layer
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0 or i == n-1 or j == n-1:
                next_surface_layer[i][j].mass = surface_layer[i][j].mass
                next_surface_layer[i][j].land = surface_layer[i][j].land
                next_surface_layer[i][j].wind = surface_layer[i][j].wind
                next_surface_layer[i][j].current = surface_layer[i][j].current
            else:
                if surface_layer[i][j].land:
                    # skpiuj wartosci z poprzedniej iteracji
                    next_surface_layer[i][j].mass = surface_layer[i][j].mass
                    next_surface_layer[i][j].land = surface_layer[i][j].land
                    next_surface_layer[i][j].wind = surface_layer[i][j].wind
                    next_surface_layer[i][j].current = surface_layer[i][j].current
                if not surface_layer[i][j].land:
                    # skopiuj wartosci z poprzedniej iteracji
                    next_surface_layer[i][j].mass = surface_layer[i][j].mass
                    next_surface_layer[i][j].land = surface_layer[i][j].land
                    next_surface_layer[i][j].wind = surface_layer[i][j].wind
                    next_surface_layer[i][j].current = surface_layer[i][j].current

                    # if neighbor is not a land:
                    # cardinal directions:
                    if not surface_layer[i - 1][j].land:# SOUTH
                        w = ((surface_layer[i][j].current[SOUTH] + surface_layer[i - 1][j].current[SOUTH]) / 2 / current_max) + \
                            R_w * ((surface_layer[i][j].wind[SOUTH] + surface_layer[i - 1][j].wind[SOUTH]) / 2 / wind_max)
                        next_surface_layer[i][j].mass += m * ((1 + w) * surface_layer[i - 1][j].mass - (1 - w) * surface_layer[i][j].mass)
                    if not surface_layer[i + 1][j].land: # NORTH
                        e = ((surface_layer[i][j].current[NORTH] + surface_layer[i + 1][j].current[NORTH]) / 2 / current_max) + \
                            R_w * ((surface_layer[i][j].wind[NORTH] + surface_layer[i + 1][j].wind[NORTH]) / 2 / wind_max)
                        next_surface_layer[i][j].mass += m * ((1 + e) * surface_layer[i + 1][j].mass - (1 - e) * surface_layer[i][j].mass)
                    if not surface_layer[i][j - 1].land: # EAST
                        s = ((surface_layer[i][j].current[EAST] + surface_layer[i][j - 1].current[EAST]) / 2 / current_max) + \
                            R_w * ((surface_layer[i][j].wind[EAST] + surface_layer[i][j - 1].wind[EAST]) / 2 / wind_max)
                        next_surface_layer[i][j].mass += m * ((1 + s) * surface_layer[i][j - 1].mass - (1 - s) * surface_layer[i][j].mass)
                    if not surface_layer[i][j + 1].land:   # WEST
                        north = ((surface_layer[i][j].current[WEST] + surface_layer[i][j + 1].current[WEST]) / 2 / current_max) + \
                                R_w * ((surface_layer[i][j].wind[WEST] + surface_layer[i][j + 1].wind[WEST]) / 2 / wind_max)
                        next_surface_layer[i][j].mass += m * ((1 + north) * surface_layer[i][j + 1].mass - (1 - north) * surface_layer[i][j].mass)

                    # intermediate directions:
                    if not surface_layer[i - 1][j - 1].land:
                        next_surface_layer[i][j].mass += m * d * (surface_layer[i - 1][j - 1].mass - surface_layer[i][j].mass)
                    if not surface_layer[i - 1][j + 1].land:
                        next_surface_layer[i][j].mass += m * d * (surface_layer[i - 1][j + 1].mass - surface_layer[i][j].mass)
                    if not surface_layer[i + 1][j - 1].land:
                        next_surface_layer[i][j].mass += m * d * (surface_layer[i + 1][j - 1].mass - surface_layer[i][j].mass)
                    if not surface_layer[i + 1][j + 1].land:
                        next_surface_layer[i][j].mass += m * d * (surface_layer[i + 1][j + 1].mass - surface_layer[i][j].mass)

    # druga petla - osadzanie na brzegu bierze wartosci z next_test wiec musi byc juz cala gotowa
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0 or i == n-1 or j == n-1:
                None
            else:
                if not surface_layer[i][j].land:
                    # jesli sasiad jest ladem i masa na tym ladzie mniejsza od max - czesc masy osadza sie na ladzie
                    # todo: m0 + P * m < C_max
                    if next_surface_layer[i - 1][j].land and next_surface_layer[i - 1][j].mass <= C_max:
                        next_surface_layer[i - 1][j].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass
                    if next_surface_layer[i + 1][j].land and next_surface_layer[i + 1][j].mass <= C_max:
                        next_surface_layer[i + 1][j].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass
                    if next_surface_layer[i][j - 1].land and next_surface_layer[i][j - 1].mass <= C_max:
                        next_surface_layer[i][j - 1].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass
                    if next_surface_layer[i][j + 1].land and next_surface_layer[i][j + 1].mass <= C_max:
                        next_surface_layer[i][j + 1].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass

                    if next_surface_layer[i - 1][j - 1].land and next_surface_layer[i - 1][j - 1].mass <= C_max:
                        next_surface_layer[i - 1][j - 1].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass
                    if next_surface_layer[i - 1][j + 1].land and next_surface_layer[i - 1][j + 1].mass <= C_max:
                        next_surface_layer[i - 1][j + 1].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass
                    if next_surface_layer[i + 1][j - 1].land and next_surface_layer[i + 1][j - 1].mass <= C_max:
                        next_surface_layer[i + 1][j - 1].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass
                    if next_surface_layer[i + 1][j + 1].land and next_surface_layer[i + 1][j + 1].mass <= C_max:
                        next_surface_layer[i + 1][j + 1].mass += P * next_surface_layer[i][j].mass
                        next_surface_layer[i][j].mass -= P * next_surface_layer[i][j].mass
    surface_layer, next_surface_layer = next_surface_layer, surface_layer


def to_matrix():
    global surface_layer, next_surface_layer
    mass_matrix = zeros([n, n])
    for i in range(n):
        for j in range(n):
            if surface_layer[i][j].land:
                mass_matrix[i, j] = (-200)
            if not surface_layer[i][j].land:
                mass_matrix[i, j] = surface_layer[i][j].mass
    if mass_matrix[10, 10] < 0:
        print("ALERT")
    return mass_matrix


def observe():
    global surface_layer, next_surface_layer
    fig, ax = plt.subplots()
    mm = to_matrix()
    ax.imshow(mm, vmin=0, vmax=1, cmap=cmap, norm=norm)
    plt.show()


initialize()

for t in range(90):
    if t % 10 == 0:
        observe()
    update()

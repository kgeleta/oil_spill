from pylab import *
from matplotlib import colors
from pprint import pprint
import matplotlib.pyplot as plt


n = 100
m = 0.098
d = 0.18
C_max = 7
P = 0.18

cmap = colors.ListedColormap(['green', 'blue', 'black'])
bounds = [(-250), (-1), 1, 2000]
norm = colors.BoundaryNorm(bounds, cmap.N)


class Cell:
    def __init__(self, mass, land):
        self.mass = mass
        self.land = land

    def __repr__(self):
        if self.land:
            return "X%.1fX" % self.mass
        else:
            return "%.1f" % self.mass


def initialize():
    global test, next_test
    test = [[Cell(0, False) for j in range(n)] for i in range(n)]
    next_test = [[Cell(0, False) for j in range(n)] for i in range(n)]
    for x in range(n):
        for y in range(n):
            if 48 < x < 52 and 36 < y < 42:
                test[x][y].land = True
            if 55 < x < 60 and 10 < y < 40:
                test[x][y].land = True
            if 45 < x < 55 and 25 < y < 35:
                test[x][y].mass = 99


def update():
    global test, next_test
    for i in range(n):
        for j in range(n):
            if i == 0 or j == 0 or i == n-1 or j == n-1:
                next_test[i][j].mass = test[i][j].mass
                next_test[i][j].land = test[i][j].land
            else:
                if test[i][j].land:
                    # skpiuj wartosci z poprzedniej iteracji
                    next_test[i][j].mass = test[i][j].mass
                    next_test[i][j].land = test[i][j].land
                if not test[i][j].land:
                    # skopiuj wartosci z poprzedniej iteracji
                    next_test[i][j].mass = test[i][j].mass
                    next_test[i][j].land = test[i][j].land
                    # jesli sasiad nie jest ladem - normalny rozklad masy
                    if not test[i-1][j].land:
                        next_test[i][j].mass += m*(test[i-1][j].mass - test[i][j].mass)
                    if not test[i+1][j].land:
                        next_test[i][j].mass += m*(test[i+1][j].mass - test[i][j].mass)
                    if not test[i][j-1].land:
                        next_test[i][j].mass += m*(test[i][j-1].mass - test[i][j].mass)
                    if not test[i][j+1].land:
                        next_test[i][j].mass += m*(test[i][j+1].mass - test[i][j].mass)

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
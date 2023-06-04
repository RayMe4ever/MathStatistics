from distribution import names
from lab1 import build_histogram
from lab2 import calc_characteristics
from lab3 import build_boxplot
from lab4 import draw_ecdf, draw_kde

if __name__ == "__main__":
    # initial conditions
    sizes = [[10, 50, 1000], [10, 100, 1000], [20, 100], [20, 60, 100]]

    # LABS
    # build_histogram(names, sizes[0])  # lab 1
    calc_characteristics(names, sizes[1])  # lab 2
    # build_boxplot(names, sizes[2])  # lab 3
    # draw_ecdf(names, sizes[3])  # lab 4.1
    # draw_kde(names, sizes[3])  # lab 4.2

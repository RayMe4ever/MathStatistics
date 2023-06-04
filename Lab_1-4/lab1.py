from matplotlib import pyplot as plt
import numpy as np
from distribution import Distribution

colors = ["deepskyblue", "limegreen", "tomato", "blueviolet", "orange"]


def build_histogram(dist_names, sizes):
    labels = ["size", "distribution"]
    line_type = "k--"
    for i, dist_name in enumerate(dist_names):
        for size in sizes:
            dist = Distribution(dist_name, size)
            dist.set_distribution()
            fig, ax = plt.subplots(1, 1)
            ax.hist(dist.random_numbers, density=True, alpha=0.7, histtype='stepfilled', color=colors[i])
            dist.set_x_pdf()
            ax.plot(dist.x, dist.pdf, line_type)
            ax.set_xlabel(labels[0] + ": " + str(size))
            ax.set_ylabel(labels[1])
            ax.set_title(dist_name)
            plt.grid()
            plt.show()

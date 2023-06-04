import statistics

import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.patches import Ellipse


class Task1:
    def __init__(self):
        self.sizes = [20, 60, 100]
        self.iterations = 1000
        self.rhos = [0, 0.5, 0.9]

    def multivar_normal(self, size, rho):
        return stats.multivariate_normal.rvs([0, 0], [[1.0, rho], [rho, 1.0]], size=size)

    def mixed_multivar_normal(self, size, rho):
        arr = 0.9 * stats.multivariate_normal.rvs([0, 0], [[1, 0.9], [0.9, 1]], size) + \
            0.1 * stats.multivariate_normal.rvs([0, 0], [[10, -0.9], [-0.9, 10]], size)
        return arr

    def quadrant_coef(self, x, y):
        x_med = np.median(x)
        y_med = np.median(y)
        n = [0, 0, 0, 0]

        for i in range(len(x)):
            if x[i] >= x_med and y[i] >= y_med:
                n[0] += 1
            elif x[i] < x_med and y[i] >= y_med:
                n[1] += 1
            elif x[i] < x_med:
                n[2] += 1
            else:
                n[3] += 1

        return (n[0] + n[2] - n[1] - n[3]) / len(x)

    def pprint(self, arr):
        st = "& "
        for a in arr:
            st += str(a)
            st += ' & '
            #print("& " + a, end=' ')
        return st

    def run(self):
        for size in self.sizes:
            for rho in self.rhos:
                mean, sq_mean, disp = self.generate_stats(self.multivar_normal, size, rho)
                print(f"Normal\t Size = {size}\t Rho = {rho}\t Mean = {self.pprint(mean)}\t Squares mean = {self.pprint(sq_mean)}\t Dispersion = {self.pprint(disp)}")

            mean, sq_mean, disp = self.generate_stats(self.mixed_multivar_normal, size, 0)
            print(f"Mixed\t Size = {size}\t Mean = {self.pprint(mean)}\t Squares mean = {self.pprint(sq_mean)}\t Dispersion = {self.pprint(disp)}")

            self.draw_ellipse(size)

    def generate_stats(self, distr_generator, size, rho):
        names = {"pearson": list(), "spearman": list(), "quadrant": list()}

        for i in range(self.iterations):
            multi_var = distr_generator(size, rho)
            x = multi_var[:, 0]
            y = multi_var[:, 1]

            names['pearson'].append(stats.pearsonr(x, y)[0])
            names['spearman'].append(stats.spearmanr(x, y)[0])
            names['quadrant'].append(self.quadrant_coef(x, y))

        mean = list()
        sq_mean = list()
        disp = list()
        for val in names.values():
            mean.append(np.median(val))
            sq_mean.append(np.median([val[k] ** 2 for k in range(self.iterations)]))
            disp.append(statistics.variance(val))

        return np.around(mean, decimals=4), np.around(sq_mean, decimals=4), np.around(disp, decimals=4)

    def build_ellipse(self, x, y, ax, n_std=3.0):
        cov = np.cov(x, y)
        pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])

        rad_x = np.sqrt(1 + pearson)
        rad_y = np.sqrt(1 - pearson)
        ellipse = Ellipse((0, 0), width=rad_x * 2, height=rad_y * 2, facecolor='none', edgecolor='navy')
        scale_x = np.sqrt(cov[0, 0]) * 3.0
        mean_x = np.mean(x)
        scale_y = np.sqrt(cov[1, 1]) * 3.0
        mean_y = np.mean(y)

        transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)
        ellipse.set_transform(transf + ax.transData)
        return ax.add_patch(ellipse)

    def draw_ellipse(self, size):
        fig, ax = plt.subplots(1, 3)
        titles = [f"rho = {rho}" for rho in self.rhos]

        for i in range(len(self.rhos)):
            sample = self.multivar_normal(size, self.rhos[i])
            x, y = sample[:, 0], sample[:, 1]
            self.build_ellipse(x, y, ax[i])
            ax[i].grid()
            ax[i].scatter(x, y, s=5)
            ax[i].set_title(titles[i])

        plt.suptitle(f"Size {size}")
        plt.show()
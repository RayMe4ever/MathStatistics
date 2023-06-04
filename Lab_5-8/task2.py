import scipy
import scipy.stats as stats
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt



class Task2:
    def __init__(self):
        self.a = -1.8
        self.b = 2
        self.step = 0.2

    def ref_func(self, x):
        return 2 * x + 2

    def depend(self, x):
        return [self.ref_func(xi) + stats.norm.rvs(0, 1) for xi in x]

    def get_least_squares_params(self, x, y):
        beta_1 = (np.mean(x * y) - np.mean(x) * np.mean(y)) / (np.mean(x * x) - np.mean(x) ** 2)
        beta_0 = np.mean(y) - beta_1 * np.mean(x)
        return beta_0, beta_1

    def least_module(self, parameters, x, y) -> float:
        alpha_0, alpha_1 = parameters
        return sum([abs(y[i] - alpha_0 - alpha_1 * x[i])
                    for i in range(len(x))])

    def get_least_module_params(self, x, y):
        beta_0, beta_1 = self.get_least_squares_params(x, y)
        result = scipy.optimize.minimize(self.least_module, [beta_0, beta_1], args=(x, y), method='SLSQP')
        return result.x[0], result.x[1]

    def least_squares_method(self, x, y):
        beta_0, beta_1 = self.get_least_squares_params(x, y)
        print(f"beta_0 = {beta_0}\t beta_1 = {beta_1}")
        return [beta_0 + beta_1 * p
                for p in x]

    def least_modules_method(self, x, y):
        alpha_0, alpha_1 = self.get_least_module_params(x, y)
        print(f"alpha_0 = {alpha_0}\t alpha_1 = {alpha_1}")
        return [alpha_0 + alpha_1 * p
                for p in x]

    def plot(self, x, y, name: str) -> None:
        y_mnk = self.least_squares_method(x, y)
        y_mnm = self.least_modules_method(x, y)

        mnk_dist = sum((self.ref_func(x)[i] - y_mnk[i]) ** 2 for i in range(len(y)))
        mnm_dist = sum(abs(self.ref_func(x)[i] - y_mnm[i]) for i in range(len(y)))
        print(f"MNK distance = {mnk_dist}\t MNM distance = {mnm_dist}")

        plt.plot(x, self.ref_func(x), color="red", label="Ideal")
        plt.plot(x, y_mnk, color="blue", label="MNK")
        plt.plot(x, y_mnm, color="green", label="MNM")
        plt.scatter(x, y, c="purple", label="Sample")
        plt.xlim([self.a, self.b])
        plt.grid()
        plt.legend()
        plt.title(name)
        plt.show()

    def run(self):
        x = np.arange(self.a, self.b, self.step)
        y = self.depend(x)
        self.plot(x, y, "Distribution")
        y[0] += 10
        y[-1] -= 10
        # y = self.depend(x)
        self.plot(x, y, "Distribution with perturbation ")

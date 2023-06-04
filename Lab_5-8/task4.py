import numpy as np
import scipy.stats as stats
from matplotlib import pyplot as plt


class Task4:
    def mean(self, data):
        return np.mean(data)

    def dispersion(self, sample):
        return self.mean(list(map(lambda x: x * x, sample))) - (self.mean(sample)) ** 2

    def normal(self, size):
        return np.random.standard_normal(size=size)

    def run(self):
        alpha = 0.05

        m_dict = {"norm": list(), "asymp": list()}
        s_dict = {"norm": list(), "asymp": list()}
        x_all = list()
        for n in [20, 100]:
            x = self.normal(n)
            x_all.append(x)
            m = self.mean(x)
            s = np.sqrt(self.dispersion(x))
            m_n = [m - s * (stats.t.ppf(1 - alpha / 2, n - 1)) / np.sqrt(n - 1),
                  m + s * (stats.t.ppf(1 - alpha / 2, n - 1)) / np.sqrt(n - 1)]
            s_n = [s * np.sqrt(n) / np.sqrt(stats.chi2.ppf(1 - alpha / 2, n - 1)),
                  s * np.sqrt(n) / np.sqrt(stats.chi2.ppf(alpha / 2, n - 1))]

            m_dict["norm"].append(m_n)
            s_dict["norm"].append(s_n)

            m_as = [m - stats.norm.ppf(1 - alpha / 2) / np.sqrt(n), m + stats.norm.ppf(1 - alpha / 2) / np.sqrt(n)]
            e = (sum(list(map(lambda el: (el - m) ** 4, x))) / n) / s ** 4 - 3
            s_as = [s / np.sqrt(1 + stats.norm.ppf(1 - alpha / 2) * np.sqrt((e + 2) / n)),
                    s / np.sqrt(1 - stats.norm.ppf(1 - alpha / 2) * np.sqrt((e + 2) / n))]

            m_dict["asymp"].append(m_as)
            s_dict["asymp"].append(s_as)

        for key in m_dict.keys():
            print(f"m {key} : {m_dict[key][0]},  {m_dict[key][1]}")
            print(f"sigma {key}: {s_dict[key][0]},  {s_dict[key][1]}")
            self.draw_result(x_all, m_dict[key], s_dict[key], key)

    def draw_result(self, x_set, m_all, s_all, name):
        fig, (ax1, ax2) = plt.subplots(1,2)

        ax1.set_ylim(0, 1)
        ax1.set_title(name)
        ax1.hist(x_set[0], density=True, histtype="stepfilled", label='n = 20')
        ax1.legend(loc='upper right')
        ax2.set_title(name)
        ax2.set_ylim(0, 1)
        ax2.hist(x_set[1], density=True, histtype="stepfilled", label='n = 100')
        ax2.legend(loc='upper right')
        fig.show()
        fig, (ax3, ax4) = plt.subplots(1,2)

        ax3.set_title(name + ' "m"')
        ax3.set_ylim(0.9, 1.4)
        ax3.plot(m_all[0], [1, 1], 'go-', label='n = 20')
        ax3.plot(m_all[1], [1.1, 1.1], 'mo-', label='n = 100')
        ax3.legend()

        ax4.set_title(name + ' "sigma"')
        ax4.set_ylim(0.9, 1.4)
        ax4.plot(s_all[0], [1, 1], 'go-', label='n = 20')
        ax4.plot(s_all[1], [1.1, 1.1], 'mo-', label='n = 100')
        ax4.legend()
        fig.show()
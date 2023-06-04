import seaborn as sns
from matplotlib import pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF

from distribution import Distribution

a, b = -4, 4
a_poisson, b_poisson = 6, 14
coefs = [0.5, 1, 2]


def draw_ecdf(dist_names, sizes):
    sns.set_style("whitegrid")
    for dist_name in dist_names:
        figures, axs = plt.subplots(ncols=3, figsize=(15, 5))
        for i, size in enumerate(sizes):
            dist, arr = prepare_to_draw(dist_name, size, 'ecdf')
            ecdf = ECDF(arr)
            axs[i].plot(dist.x, dist.cdf, color="blue", label="cdf")
            axs[i].plot(dist.x, ecdf(dist.x), color="red", label="ecdf")
            axs[i].legend(loc='lower right')
            axs[i].set(xlabel="x", ylabel="F(x)")
            axs[i].set_title(f"n = {size}")
        figures.suptitle(dist_name)
        plt.show()


def draw_kde(dist_names, sizes):
    sns.set_style("whitegrid")
    for dist_name in dist_names:
        for size in sizes:
            figures, axs = plt.subplots(ncols=3, figsize=(15, 5))
            dist, arr = prepare_to_draw(dist_name, size, 'kde')
            for i, coef in enumerate(coefs):
                axs[i].plot(dist.x, dist.pdf, color="red", label="pdf")
                sns.kdeplot(data=arr, bw_method="silverman", bw_adjust=coef, ax=axs[i], fill=True, linewidth=0, label="kde")
                axs[i].legend(loc="upper right")
                axs[i].set(xlabel="x", ylabel="f(x)")
                axs[i].set_xlim([dist.a, dist.b])
                axs[i].set_title("h = " + str(coef))
            figures.suptitle(f"{dist_name} KDE n = {size}")
            plt.show()


def prepare_to_draw(dist_name, size, param):
    dist = Distribution(dist_name, size)
    dist.set_a_b(a, b, a_poisson, b_poisson)
    dist.set_distribution()
    dist.set_x_cdf_pdf(param)
    arr = sorted(dist.random_numbers)
    return dist, arr






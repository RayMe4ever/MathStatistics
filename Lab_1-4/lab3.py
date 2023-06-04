import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from distribution import Distribution


def build_boxplot(dist_names, sizes):
    for dist_name in dist_names:
        tips = []
        for size in sizes:
            dist = Distribution(dist_name, size)
            emission_share(dist, dist.repeat_num)
            tips.append(dist.random_numbers)
        draw_boxplot(dist_name, tips)


def mustache(distribution):
    q_1, q_3 = np.quantile(distribution, [0.25, 0.75])
    return q_1 - 3 / 2 * (q_3 - q_1), q_3 + 3 / 2 * (q_3 - q_1)


def count_emissions(distribution):
    x1, x2 = mustache(distribution)
    filtered = [x for x in distribution if x > x2 or x < x1]
    return len(filtered)


def emission_share(dist, repeat_num):
    count = 0
    for i in range(repeat_num):
        dist.set_distribution()
        arr = sorted(dist.random_numbers)
        count += count_emissions(arr)
    count /= (dist.size * repeat_num)
    dist.set_distribution()
    print(f"{dist.name} Size {dist.size}: {count}")


def draw_boxplot(dist_name, data):
    sns.set_theme(style="whitegrid")
    sns.boxplot(data=data, palette='pastel', orient='h')
    sns.despine(offset=10)
    plt.xlabel("x")
    plt.ylabel("n")
    plt.title(dist_name)
    # plt.savefig(img_path)
    plt.show()


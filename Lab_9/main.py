from json import load
# from optparse import Values

import numpy as np
from load_data import load_from_csv, load_octave
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as opt


def plot_data(data):
    for d in data:
        x = range(1, d.values[:, 0].size + 1)
        y = d.values[:, 0]
        
        for i in range(len(x) - 1):
            plt.plot([x[i], x[i+1]], [y[i], y[i]], color='m')
    
    plt.xlabel('n')
    plt.ylabel('mV')
    plt.title("Experiment data")
    plt.savefig("../image/data.png")
    # plt.show()


def plot_interval(data, part):
    x = range(1, data[:, 0].size + 1)
    x2 = np.array(range(1, data[:, 0].size + 1))
    mask = (data[:, 0] < 0.9196246) & (data[:, 1] > 0.919663)
    y_min = np.maximum(data[:, 1], 0.9196246)  # Lower limit for the interval
    y_max = np.minimum(data[:, 0], 0.919663)   # Upper limit for the interval
    
    if part == 2 and np.any(mask):
        plt.vlines(x, data[:, 0], data[:, 1], colors="g")              # Plot the whole interval with cyan
        plt.vlines(x2[mask], y_min[mask], y_max[mask], colors="m")  # Plot the interval within the condition with hotpink
    elif part == 3:
        plt.vlines(x, data[:, 0], data[:, 1], colors="g")
        plt.hlines(0.919603, 0, 200, colors="m", lw=2)
    else:
        plt.vlines(x, data[:, 0], data[:, 1], colors="g")  # Plot the whole interval with cyan


def wrapper_plot_interval(data, eps, part, label="Data intervals"):
    for i in range(len(data)):
        data[i].values[:, 1] = data[i].values[:, 0] + eps
        data[i].values[:, 0] -= eps
        plot_interval(data[i].values, part)
    
    plt.xlabel('n')
    plt.ylabel('mV')
    plt.title(label)
    plt.savefig(f"../image/data_and_intervals{part}.png")
    plt.show()


def find_mu(data, interval, eps):
    count = 0
    for i in range(len(data)):
        if ((data[i].values[:, 0] + eps) > interval[1]).any() and ((data[i].values[:, 0] - eps) < interval[0]).any():
            count += 1
    return count



def find_all_mu(data, z, eps):
    mu = []
    for i in range(len(z)):
        mu.append(find_mu(data, z[i], eps))
    return mu


def find_down_min(data, eps):
    min_val = data[0].values[:, 0] - eps
    for i in range(len(data)):
        if data[i].values[:, 0] - eps < min_val:
            min_val = data[i].values[:, 0] - eps
    return min_val


def find_down_max(data, eps):
    max_val = data[0].values[:, 0] - eps
    for i in range(len(data)):
        if data[i].values[:, 0] - eps > max_val:
            max_val = data[i].values[:, 0] - eps
    return max_val


def find_up_min(data, eps):
    max_val = data[0][:, 0] - eps
    for i in range(len(data)):
        if data[i][:, 0] - eps > max_val:
            max_val = data[i][:, 0] - eps
    return max_val


def find_up_max(data, eps):
    max_val = data[0].values[:, 0] - eps
    for i in range(len(data)):
        if data[i].values[:, 0] + eps > max_val:
            max_val = data[i].values[:, 0] - eps
    return max_val


def plot_mu(data, eps):
    up_count = 0
    down_count = 0
    tmp_z = []
    for i in range(2 * len(data)):
        n = len(data)
        if n > 0:
            down_count = 0
            up_count = n - 1
            # print(size_range(data))
            if (data[down_count].values[:, 0] - eps < data[up_count].values[:, 0] + eps).any():
                tmp_z.append(data[down_count].values[:, 0] - eps)
                down_count = down_count + 1
            else:
                tmp_z.append(data[up_count].values[:, 0] + eps)
                up_count = up_count + 1
        else:
            tmp_z.append(data[up_count].values[:, 0] + eps)
            up_count = up_count + 1

    z = []
    for i in range(len(tmp_z) - 1):
        z.append([tmp_z[i], tmp_z[i + 1]])

    mu = find_all_mu(data, z, eps)
    mV = []
    mx = max(mu)
    print(mx)

    maxIntervals = []
    for i in range(len(mu)):
        if mu[i] == mx:
            maxIntervals.append([z[i][0], z[i][1]])
            print(i+1)

    down_max = find_down_max(maxIntervals, eps)
    up_min = find_up_min(maxIntervals, eps)
    down_min = find_down_max(data, eps)
    up_max = find_up_min(data, eps)
    print((up_min - down_max) / (up_max - down_min))
    print(maxIntervals[0][0], maxIntervals[len(maxIntervals) - 1][1])
    plt.axis([0.9189, 0.9206, 0, 55])
    for i in range(len(z)):
        mV.append((z[i][0] + z[i][1]) / 2)

    plt.plot(mV, mu)
    plt.hlines(max(mu), 0.9189, 0.9206, 'hotpink', '--')
    plt.title('Mu_calculations')
    plt.xlabel('mV')
    plt.ylabel('mu')
    plt.savefig("input_mu.png")
    plt.figure()




if __name__ == "__main__":
    data = []
    data.append(load_from_csv("data/Chanel_1_400nm_2mm.csv"))
    plot_data(data)

    eps = 1e-4
    size_range = range(len(data))
    wrapper_plot_interval(data, eps, 1)
    wrapper_plot_interval(data, eps, 2)
    wrapper_plot_interval(data, eps * 7.7490, 3)
    # plot_mu(data, eps)
    # a, b, w = [], [], []
    # for i in size_range:
    #     a_tmp, b_tmp, w_tmp = load_octave(f"data/Chanel.txt")
    #     a.append(a_tmp)
    #     b.append(b_tmp)
    #     w.append(w_tmp)

    # for i in size_range:
    #     data[i].values[:, 1] += (eps * pd.DataFrame(w[i])).values[:, 0]
    #     data[i].values[:, 0] -= (eps * pd.DataFrame(w[i])).values[:, 0]

    # for i in size_range:
    #     plt.hist(w[i], histtype="stepfilled", color="m")
    #     plt.xlabel('w')
    #     plt.ylabel('N')
    #     plt.title(f'w Chanel_1_400nm_2mm.csv')
    #     plt.savefig(f"../image/hist{i + 1}.png")
    #     plt.figure()

    # for i in size_range:
    #     plot_interval(data[i].values)
    #     plt.plot([1, 200], [1 * b[i] + a[i], 200 * b[i] + a[i]])
    #     plt.title(f'Chanel_1_400nm_2mm.csv')
    #     plt.xlabel('n')
    #     plt.ylabel('mV')
    #     plt.savefig(f"../image/di{i + 1}.png")
    #     plt.figure()

    # data_fixed = []
    # for i in size_range:
    #     x = pd.DataFrame(range(1, data[i].values[:, 0].size + 1))
    #     plt.vlines(x.values[:, 0], data[i].values[:, 0] - b[i] * x.values[:, 0],
    #                data[i].values[:, 1] - b[i] * x.values[:, 0], colors="c")
    #     plt.plot([x.values[:, 0][0], x.values[:, 0][-1]], [a[i], a[i]], color='blue')
    #     plt.title(f'Chanel_1_400nm_2mm.csv')
    #     plt.xlabel('n')
    #     plt.ylabel('mV')
    #     plt.savefig(f"../image/interval_new{i + 1}.png")
    #     plt.figure()
    #     data_fixed.append([data[i].values[:, 0] - b[i] * x.values[:, 0], data[i].values[:, 1] - b[i] * x.values[:, 0]])

    # for i in size_range:
    #     x = pd.DataFrame(range(1, data[i].values[:, 0].size + 1))
    #     plt.hist((data_fixed[i][0] + data_fixed[i][1]) / 2, color="m")
    #     plt.xlabel('mV')
    #     plt.ylabel('N')
    #     plt.title(f'Chanel_1_400nm_2mm.csv')
    #     plt.savefig(f"../image/hist_interval{i + 1}.png")
    #     plt.figure()

    # R_interval = [0.001 * i + 1 for i in range(150)]
    # Jaccars = []


    # def countJakkar(R):
    #     data1_new = [[data_fixed[0][0][i] * R, data_fixed[0][1][i] * R] for i in range(200)]
    #     all_data = data1_new + [[data_fixed[1][0][i], data_fixed[1][1][i]] for i in range(200)]
    #     min_inc = list(all_data[0])
    #     max_inc = list(all_data[0])
    #     for interval in all_data:
    #         min_inc[0] = max(min_inc[0], interval[0])
    #         min_inc[1] = min(min_inc[1], interval[1])
    #         max_inc[0] = min(max_inc[0], interval[0])
    #         max_inc[1] = max(max_inc[1], interval[1])
    #     JK = (min_inc[1] - min_inc[0]) / (max_inc[1] - max_inc[0])
    #     return JK


    # for R in R_interval:
    #     Jaccars.append(countJakkar(R))

    # optimal_x = opt.fmin(lambda x: -countJakkar(x), 0)
    # print(optimal_x[0])

    # min1 = opt.root(countJakkar, 1)
    # max1 = opt.root(countJakkar, 3)
    # print(min1.x, max1.x)

    # plt.plot(R_interval, Jaccars, zorder=1, color="cyan")
    # plt.scatter(optimal_x[0], countJakkar(optimal_x[0]), color="r")
    # plt.scatter(min1.x, countJakkar(min1.x), label="$min R$=" + str(min1.x[0])[0:7], color="m", zorder=2)
    # plt.scatter(max1.x, countJakkar(max1.x), label="$max R$=" + str(max1.x[0])[0:7], color="m", zorder=2)
    # plt.legend()
    # plt.xlabel('$R_{21}$')
    # plt.ylabel('Jaccard')
    # plt.title('Jaccard vs R')
    # plt.savefig("../image/jakkar.png")
    # plt.figure()

    # data1_new = [[data_fixed[0][0][i] * optimal_x[0], data_fixed[0][1][i] * optimal_x[0]] for i in range(200)]
    # all_data = data1_new + [[data_fixed[1][0][i], data_fixed[1][1][i]] for i in range(200)]
    # plt.xlabel('mV')
    # plt.ylabel('N')
    # plt.hist([(x[0] + x[1]) / 2 for x in all_data], density=True, color="m")
    # plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 1))
    # plt.savefig("../image/jakkar_combined_hist.png")
import numpy as np
import matplotlib.pyplot as plt
import datetime


def plot(curve_paires: list, time):
    for pair in curve_paires:
        for c in pair:
            if (c.__contains__('empleando')):
                plt.plot(time, pair[c], label=f'{c}', linestyle='--')
            else:
                plt.plot(time, pair[c], label=f'{c}')

        plt.legend()
        plt.show()


def plot_values(data_org, data_est, time, label_y1, label_y2):
    plt.plot(time, data_org,
             label=label_y1, linestyle='--')
    plt.plot(time, data_est, label=label_y2)
    plt.xlabel("tiempo en días")
    plt.ylabel("activos por día")
    plt.legend()
    plt.show()


def sigle_plot_and_itresting_points(x, y, points: list, dates: list):
    plt.plot(x, y, label='I(t) estimado')
    for i, point in enumerate(points):
        p_x = point[0]
        p_y = point[1]
        plt.plot(p_x, p_y, marker="o", color="green",
                 label=f'p{i}: {dates[i]}')
        if i != 1:
            plt.annotate(f'p{i}{(point[0], int(point[1]))}',
                         (point[0], point[1]),
                         textcoords="offset points",
                         xytext=(0, 3),
                         ha='center')
        else:
            plt.annotate(f'p{i}{(point[0], int(point[1]))}',
                         (point[0], point[1]),
                         textcoords="offset points",
                         xytext=(33, -8),
                         ha='center')
    plt.xlabel("tiempo en días")
    plt.ylabel("activos por día")
    plt.legend()
    plt.show()


def get_points_in_range(ranges: list, data, min_maxs: list):
    points = []
    for i, min_max in enumerate(min_maxs):
        if min_max == -1:
            best = np.inf
        else:
            best = -np.inf

        start = ranges[i][0]
        end = ranges[i][1]
        day = 0
        while start <= end:
            if min_max == -1 and data[start] < best:
                best = data[start]
                day = start
            elif min_max == 1 and data[start] > best:
                best = data[start]
                day = start
            start += 1
        points.append((day, best))
    return points


def build_labels_for_especial_points(points: list, start_date: datetime.date):
    return [start_date + datetime.timedelta(days=p[0]) for p in points]

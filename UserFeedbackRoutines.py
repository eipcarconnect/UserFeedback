import sched
import time
import os.path
from datetime import date, datetime
from statistics import mean
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from UserFeedbackHelper import *


def routine():
    with open(FORM_PATH, "r") as f:
        lines = f.readlines()[1:]
        today = []
        for line in lines:
            split = line.split('\t')
            if split[0] == date.today().strftime("%d/%m/%Y"):
                print(split)
                today.append(float(split[3]))
        with open(STAT_PATH, "a") as e:
            e.write(date.today().strftime("%d/%m/%Y") + '\t' + str(len(today)) + '\t' + str(mean(today)) + '\n')
            e.flush()
            e.close()

        print("Average " + date.today().strftime("%d/%m/%Y") + " => " + str(mean(today)))
        f.close()

    s.enter(86400, 1, routine)


def graph():
    with open(STAT_PATH, "r") as f:
        lines = [line.split('\t') for line in f.readlines()[1:]]
        f.close()
        dates = [elem[0] for elem in lines]
        x_values = [datetime.strptime(d, "%d/%m/%Y").date() for d in dates]
        y_values = [elem[2] for elem in lines]

        ax = plt.gca()

        formatter = mdates.DateFormatter("%d/%m/%Y")

        ax.xaxis.set_major_formatter(formatter)

        locator = mdates.DayLocator()

        ax.xaxis.set_major_locator(locator)

        plt.plot(x_values, y_values)
        plt.savefig('graph.png')
        plt.show()

    s.enter(86400, 1, graph)


if __name__ == '__main__':
    if not os.path.isfile(STAT_PATH):
        with open(STAT_PATH, 'w+') as c:
            c.write('\t'.join(STAT_TABLE) + '\n')
            c.flush()
            c.close()

    s = sched.scheduler(time.time, time.sleep)
    s.enter(86400, 1, routine)
    s.enter(86400, 1, graph)
    s.run()

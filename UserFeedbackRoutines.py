import sched
import time
import os.path
from datetime import date
from statistics import mean

from UserFeedbackHelper import *


def routine():
    print("Doing stuff...")
    with open(FORM_PATH, "r") as f:
        lines = f.readlines()[1:]
        today = []
        for line in lines:
            split = line.split('\t')
            if split[0] == date.today().strftime("%d/%m/%Y"):
                print(split)
                today.append(float(split[3]))
        with open(STAT_PATH, "w+") as e:
            e.write(date.today().strftime("%d/%m/%Y") + '\t' + str(len(today)) + '\t' + str(mean(today)) + '\n')
            e.flush()
            e.close()
        f.close()

    s.enter(5, 1, routine)


if __name__ == '__main__':
    if not os.path.isfile(STAT_PATH):
        with open(STAT_PATH, 'w+') as c:
            c.write('\t'.join(STAT_TABLE) + '\n')
            c.flush()
            c.close()

    s = sched.scheduler(time.time, time.sleep)
    s.enter(5, 1, routine)
    s.run()

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import scipy as sp
from matplotlib.animation import FuncAnimation
import random as r
import pyvisa
import argparse
import os
import time
from fos import SerialFos
from matplotlib.ticker import FormatStrFormatter, StrMethodFormatter

from wavemeterTelnet import Wavemeter


def grapher(switches, pollTime):
    try:
        print("connect to wavemeter")
        wm = Wavemeter()
    except IndexError:
        print("Index Error")
    ques = True
    # define and adjust figure

    # Temporary
    pollTime = pollTime * 10

    plots = []
    number_of_subplots = len(switches)
    fig = plt.figure(figsize=(11,7), facecolor='#DEDEDE')
    stats = plt.figure(figsize=(4.5,6))
    statblock = stats.add_subplot()
    statblock.axis('off')
    plt.rc('ytick', labelsize=7)
    for i in range(0, number_of_subplots):
        plots.append(fig.add_subplot(number_of_subplots, 1, i + 1))
        plots[i].set_title("Switch " + (str(switches[i])))

    fig.subplots_adjust(left=0.15,
                        bottom=0.1,
                        right=0.95,
                        top=0.9,
                        wspace=0.5,
                        hspace=.5)

    for i in range(0, len(plots)):
        workingPlot = plots[i]
        freq = []
        for j in range(0, pollTime + 1):
            freq.append(wm.query(b':MEAS:FREQ?'))
            #freq.append(729.4734605 + r.randint(1, 6) * .0000001)
            # time.sleep(.1)
            if r.randint(1, 3) == 2:
                scatterIdx = j

        workingPlot.set_facecolor('#DEDEDE')
        workingPlot.set_xlabel("Time")
        workingPlot.set_ylabel("Frequency")
        workingPlot.xaxis.set_ticks(np.arange(0, pollTime + 1, 100))
        workingPlot.xaxis.set_ticklabels(np.arange(0, (pollTime/10) + 1, 10))
        workingPlot.set_ylim(min(freq) - .0000004, max(freq) + .0000004)
        workingPlot.yaxis.set_major_formatter(matplotlib.ticker.EngFormatter(unit='THz', places=7))
        #workingPlot.xaxis.set_major_formatter(matplotlib.ticker.EngFormatter(unit='s'))
        workingPlot.errorbar(list(range(0, len(freq))), freq, yerr=.0000002)
        workingPlot.scatter(scatterIdx, freq[scatterIdx], c="red", zorder=100)

        statblock.text(0, .9 - i / len(switches),
                       "avg: " + str(round(np.average(freq), 7)) + " THz")
        statblock.text(.5, .9 - i / len(switches), "std: " + str(round(100000000 * np.std(freq), 7)) + " kHz")
    if ques:
        statblock.text(0, 0, "ALERT: QUES bit is set")
    plt.show()

    # Reminder that animation is possible
    # self.ani = FuncAnimation(self.fig, self.my_function, interval=100)


def main():
    parser = argparse.ArgumentParser(description='Interface with the 228A.')
    parser.add_argument("-f", "--function", help="eventually specify what task you want",
                        choices=["draw", "switch", "reset"])
    parser.add_argument("--time", help="set poll time per switch in seconds, default is 60")
    parser.add_argument("-s", "--switch", help="set gate to switch to", nargs="+", type=int)
    args = parser.parse_args()
    if args.function == "draw" or not args.function:
        if not args.time:
            pollTime = 60
        else:
            pollTime = int(args.time)
        if not args.switch:
            switches = [1, 2, 3]
        else:
            switches = args.switch
        grapher(switches, pollTime)

    elif args.function == "switch":
        if not args.switch:
            switch = 1
        else:
            switch = args.switch
        fos = SerialFos()
        fos.change_channel(switch)
        print("switching to " + str(switch))
    elif args.function == "reset":
        print("resetting the thing")


if __name__ == "__main__":
    main()

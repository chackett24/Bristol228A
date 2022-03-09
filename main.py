import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from matplotlib.animation import FuncAnimation
import random as r
import pyvisa
import argparse
#from bristol_fos import FOS
#from bristol_wavemeter import Wavemeter


class Grapher():
    def __init__(self):
        # start collections with zeros
        self.freq = [5]
        self.power = [5]
        self.time = [0]
        # define and adjust figure
        self.fig = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
        self.plot1 = self.fig.add_subplot(221)
        self.plot2 = self.fig.add_subplot(222)
        self.plot3 = self.fig.add_subplot(223)
        self.plot4 = self.fig.add_subplot(224)

        self.plot1.set_facecolor('#DEDEDE')
        self.plot2.set_facecolor('#DEDEDE')

        # function to update the data
    def my_function(self, i):
        # get data
        self.freq.append(self.freq[-1] + r.randint(-10, 10))
        self.power.append(self.power[-1] + r.randint(-10, 10))
        # clear axis
        self.plot1.cla()
        self.plot2.cla()
        self.plot3.cla()
        self.plot4.cla()
        # plot cpu
        self.plot1.plot(self.freq)
        self.plot3.text(.5, 2 / 3, '%.1f' % np.average(self.freq), horizontalalignment='center',
                        verticalalignment='center')
        self.plot3.text(.5, 1 / 3, '%.1f' % np.std(self.freq), horizontalalignment='center',
                        verticalalignment='center')
        self.plot1.errorbar(list(range(0, len(self.freq))), self.freq, yerr=5)
        # ax.scatter(len(freq) - 1, freq[-1])
        # ax.text(len(freq) - 1, freq[-1] + 2, "{}%".format(freq[-1]))
        self.plot1.set_ylim(min(self.freq) - 5, max(self.freq) + 10)

        # plot power
        self.plot2.plot(self.power)
        self.plot4.text(.5, 2 / 3, '%.1f' % np.average(self.power), horizontalalignment='center',
                        verticalalignment='center')
        self.plot4.text(.5, 1 / 3, '%.1f' % np.std(self.power), horizontalalignment='center',
                        verticalalignment='center')
        self.plot2.errorbar(list(range(0, len(self.power))), self.power, yerr=5)
        self.plot2.set_ylim(min(self.power) - 5, max(self.power) + 10)


def main():
    parser = argparse.ArgumentParser(description='Interface with the 228A.')
    parser.add_argument("-f", "--function", help="eventually specify what task you want",
                        choices=["draw", "switch", "reset"])
    parser.add_argument("--tick", help="set tick rate in ms, default is 10")
    parser.add_argument("-s", "--switch", help="set gate to switch to", type=int)
    args = parser.parse_args()
    if args.function == "draw" or not args.function:
        grapher = Grapher()
        if not args.tick:
            tick = 10
        else:
            tick = args.tick
        ani = FuncAnimation(grapher.fig, grapher.my_function, interval=tick)
        plt.show()
    elif args.function == "switch":
        if not args.switch:
            switch = 1
        else:
            switch = args.switch
        #fos = FOS()
        #fos.change_channel(switch)
        print("switching to " + str(switch))
    elif args.function == "reset":
        print("resetting the thing")


if __name__ == "__main__":
    main()

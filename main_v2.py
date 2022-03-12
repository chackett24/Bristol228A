import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from matplotlib.animation import FuncAnimation
import random as r
import pyvisa
import argparse
import os
import time
#from bristol_fos import FOS
from bristol_wavemeter import Wavemeter


class Grapher():
    def __init__(self, switches):
        try:
            print("oops")
            #self.wm = Wavemeter()
        except IndexError:
            print("bad")
        # start collections with zeros
        self.freq = [500]
        self.power = [500]
        self.ques = True
        self.time = 60
        self.countdown = self.time
        self.switches = switches
        self.working_plot = 0
        # define and adjust figure
        self.plots = []
        number_of_subplots = len(self.switches)
        self.fig = plt.figure(facecolor='#DEDEDE')
        self.stats = plt.figure()
        self.statblock = self.stats.add_subplot()
        self.statblock.axis('off')
        #plot1 = self.fig.add_subplot(221)
        for i in range(0,number_of_subplots):
            self.plots.append(self.fig.add_subplot(number_of_subplots,1,i+1))
            self.plots[i].set_title("Switch "  + (str(self.switches[i])))

        for plot in self.plots:
            plot.set_facecolor('#DEDEDE')

        self.fig.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.9,
                            top=0.9,
                            wspace=0.4,
                            hspace=.5)

        for i in range(0,len(self.plots)):
            workingPlot = self.plots[i]
            self.freq = [500]
            for j in range(0,self.time):
                self.freq.append(self.freq[-1] + r.randint(-1, 1))
                #workingPlot.set_title(" Plot")
                #time.sleep(.1)
                if 510> self.freq[-1] > 490:
                    workingPlot.cla()
                    workingPlot.scatter(len(self.freq) - 1, self.freq[-1])
            workingPlot.errorbar(list(range(0, len(self.freq))), self.freq, yerr=1)
            workingPlot.set_ylim(min(self.freq) - 2, max(self.freq) + 2)
            self.statblock.text(.1, .9 - (i)/len(self.switches),"avg: " + str(round(np.average(self.freq), 4)))
            self.statblock.text(.6, .9 - (i) / len(self.switches), "std: " + str(round(np.std(self.freq), 4)))
        if self.ques:
            self.statblock.text(0, 0, "ALERT: QUES bit is set")
        plt.show()

        #self.ani = FuncAnimation(self.fig, self.my_function, interval=100)
        #self.ani.running = True

        # function to update the data


    """def my_function(self, i):
        self.countdown -= 1
        if self.countdown == 0:
            self.countdown = self.time
            self.working_plot += 1
            self.freq = [r.randint(-30, 30)]

        if self.working_plot >= len(self.plots):
            self.ani.event_source.stop()
        else:
            # get data
            self.freq.append(self.freq[-1] + r.randint(-30, 30))
            self.power.append(self.power[-1] + r.randint(-30, 30))
            # clear axis
            self.plots[self.working_plot].cla()
            # plot cpu
            self.plots[self.working_plot].set_title((str(self.switches[self.working_plot]) + " Plot"))
            self.plots[self.working_plot].plot(self.freq)
            self.plots[self.working_plot].errorbar(list(range(0, len(self.freq))), self.freq, yerr=30)
            self.plots[self.working_plot].set_ylim(min(self.freq) - 5, max(self.freq) + 10)
            #self.plot1.plot(self.freq)
            #self.plot3.text(.5, 2 / 3, '%.1f' % np.average(self.freq), horizontalalignment='center',verticalalignment='center')
            #self.plot3.text(.5, 1 / 3, '%.1f' % np.std(self.freq), horizontalalignment='center',verticalalignment='center')
            # ax.scatter(len(freq) - 1, freq[-1])
            # ax.text(len(freq) - 1, freq[-1] + 2, "{}%".format(freq[-1]))
            #self.plot1.set_ylim(min(self.freq) - 5, max(self.freq) + 10)

            # plot power"""



def main():
    parser = argparse.ArgumentParser(description='Interface with the 228A.')
    parser.add_argument("-f", "--function", help="eventually specify what task you want",
                        choices=["draw", "switch", "reset"])
    parser.add_argument("--tick", help="set tick rate in ms, default is 10")
    parser.add_argument("-s", "--switch", help="set gate to switch to", nargs="+", type=int)
    args = parser.parse_args()
    if args.function == "draw" or not args.function:
        if not args.tick:
            tick = 10
        else:
            tick = args.tick
        if not args.switch:
            switches = [1,2,3]
        else:
            switches = args.switch
        grapher = Grapher(switches)

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

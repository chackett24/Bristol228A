import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyvisa

class Wavemeter:
    def __init__(self):
        # see https://pyvisa.readthedocs.io/en/latest/introduction/communication.html#an-example
        rm = pyvisa.ResourceManager()  # VISA backend
        print(rm.list_resources)
        instr = rm.list_resources()  # resource list
        print((instr))
        self.device = rm.open_resource(instr[0])  # find the instrument
        self.device.baud_rate = 921600 # 9600
        self.device.write_termination = "\n"
        self.device.read_termination = "\n"

        print(self.device)
        print(self.device.query('*IDN?'))  # query instrument id

    def get_power(self):
        return self.device.query(':READ:POWer?')


    def get_freq(self):
        return self.device.query(':MEAS:FREQ?')

    def diagnostics(self):
        print(self.device.write(':DISPlay:DIALog MAIN'))  # select main display screen
        print(self.device.query(':READ:POWer?'))  # power
        print(self.device.query(':DISPlay:UNITs:POWer?'))
        print( )  # frequency
        print(self.device.query(':DISPlay:UNITs:WAVelength?'))

        print(self.device.query(':MEAS:FREQ?'))  # 'MEAS' initiates a new reading and return the value when the reading is complete.
        print(self.device.query(':DISPlay:UNITs:WAVelength?'))


if __name__ == '__main__':
    wm = Wavemeter()

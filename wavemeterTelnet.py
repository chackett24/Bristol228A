from telnetlib import Telnet

class Wavemeter:
    def __init__(self):
        self.tn = Telnet("192.168.1.88")


        print(self.device)
        print(self.device.write('*IDN?'))  # query instrument id

    def query(self, command):
        self.tn.write(command)
        return self.tn.read_eager()


    def get_power(self):
        return self.query(':READ:POWer?')


    def get_freq(self):
        return self.query(':MEAS:FREQ?')


    def diagnostics(self):
        print(self.query(b':READ:POWer?'))  # power
        print(self.query(b':DISPlay:UNITs:POWer?'))
        print(self.query(b':DISPlay:UNITs:WAVelength?'))

        print(self.query(b':MEAS:FREQ?'))  # 'MEAS' initiates a new reading and return the value when the reading is complete.
        print(self.query(b':DISPlay:UNITs:WAVelength?'))

if __name__ == "__main__":
    wm = Wavemeter()
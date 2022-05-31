from telnetlib import Telnet
import time

class Wavemeter:
    def __init__(self):
        self.tn = Telnet("192.168.1.88", timeout = 10)

    def query(self, command):
        self.tn.write(command)
        time.sleep(1)
        return self.tn.read_very_eager().decode().rstrip("\r\n")


    def get_power(self):
        self.tn.write(b':MEAS:POWer?\n')
        return self.tn.read_until(b"\r\n").decode().strip("\r\n")

    def get_freq(self):
        self.tn.write(b':MEAS:FREQ?\n')
        return self.tn.read_until(b"\r\n").decode().strip("\r\n")


    def diagnostics(self):
        print(self.query(b':READ:POWer?'))  # power
        print(self.query(b':DISPlay:UNITs:POWer?'))
        print(self.query(b':DISPlay:UNITs:WAVelength?'))

        print(self.query(b':MEAS:FREQ?'))  # 'MEAS' initiates a new reading and return the value when the reading is complete.
        print(self.query(b':DISPlay:UNITs:WAVelength?'))

if __name__ == "__main__":
    wm = Wavemeter()
    print(wm.query(b"*IDN?\n"))

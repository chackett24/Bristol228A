import serial
import time

class SerialFos:

    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 57600
        self.ser.port = 'COM3'
        self.ser.timeout = None
        print(self.ser)
        self.ser.open()

    def change_channel(self, channel):
        """ Change the fiber optic channel - choose 0,1,2,3"""
        if channel in [0, 1, 2, 3, 4, 5, 6, 7]:
            command = "ch" + str(channel) + "\r\n"
            self.ser.write(command.encode())
            self.ser.write(b'ch?\r\n')
            ret = self.ser.read(size=1)
            print(ret.decode())
        else:
            print("Invalid channel")

if __name__ == '__main__':
    fos = SerialFos()
    fos.change_channel(2)

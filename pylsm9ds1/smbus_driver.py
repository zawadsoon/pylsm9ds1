import smbus

class SMBusDriver:
    
    def __init__ (self, address, bus_number = 1, debug = False):
        self.smbus = smbus.SMBus(bus_number)
        self.debug = debug
        self.address = address
        #Debug message
        if self.debug:
            print("Conecting to IMU on bus " + str(self.bus_number))

    def close (self):
        self.smbus.close()
        #Debug message
        if self.debug:
            print("Closing IMU on bus " + str(self.bus_number))

    def readReg (self, reg):
        return self.smbus.read_byte_data(self.address, reg)

    def writeReg (self, reg, value):
        self.smbus.write_byte_data(self.address, reg, value)

    def readValue (self, regL, regH):
        return int.from_bytes([
            self.readReg(regH),
            self.readReg(regL)
        ], byteorder = 'big', signed = True)

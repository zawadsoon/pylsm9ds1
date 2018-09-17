class MAG:
    ADDRESS = 0x1e
    WHO_AM_I = 0x0F
    WHO_AM_I_OK = 0x3D
    OFFSET_X_REG_L_M = 0x05
    OFFSET_X_REG_H_M = 0x06
    OFFSET_Y_REG_L_M = 0x07
    OFFSET_Y_REG_H_M = 0x08
    OFFSET_Z_REG_L_M = 0x09
    OFFSET_Z_REG_H_M = 0x0A
    CTRL_REG1_M = 0x20
    CTRL_REG2_M = 0x21
    CTRL_REG3_M = 0x22
    CTRL_REG4_M = 0x23
    CTRL_REG5_M = 0x24
    STATUS_REG_M = 0x27
    OUT_X_L_M = 0x28
    OUT_X_H_M = 0x29
    OUT_Y_L_M = 0x2A
    OUT_Y_H_M = 0x2B
    OUT_Z_L_M = 0x2C
    OUT_Z_H_M = 0x2D
    INT_CFG_M = 0x30
    INT_SRC_M = 0x31
    INT_TSH_L_M = 0x32
    INT_TSH_H_M = 0x33

    def __init__ (self, driver = None):
        self.driver = driver

    def whoAmI (self):
        return self.driver.readReg(self.WHO_AM_I)

    def selfTest (self):
        return self.whoAmI() == self.WHO_AM_I_OK

    def enable (self):
        self.driver.writeReg(self.CTRL_REG1_M, 0x5C)
        self.driver.writeReg(self.CTRL_REG2_M, 0x60)
        self.driver.writeReg(self.CTRL_REG3_M, 0x00)

    def read (self):
        x = self.driver.readValue(self.OUT_X_L_M, self.OUT_X_L_M)
        y = self.driver.readValue(self.OUT_Y_L_M, self.OUT_Y_L_M)
        z = self.driver.readValue(self.OUT_Z_L_M, self.OUT_Z_L_M)
        return x, y, z

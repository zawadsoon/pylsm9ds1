class ACC_GYRO:
    ADDRESS = 0x6B
    WHO_AM_I = 0x0F
    WHO_AM_I_OK = 0x68
    ACT_THS = 0x04
    ACT_DUR = 0x05
    INT_GEN_CFG_XL = 0x06
    INT_GEN_THS_X_XL = 0x07
    INT_GEN_THS_Y_XL = 0x08
    INT_GEN_THS_Z_XL = 0x09
    INT_GEN_DUR_XL = 0x0A
    REFERENCE_G = 0x0B
    INT1_CTRL = 0x0C
    INT2_CTRL = 0x0D
    CTRL_REG1_G = 0x10
    CTRL_REG2_G = 0x11
    CTRL_REG3_G = 0x12
    ORIENT_CFG_G = 0x13
    INT_GEN_SRC_G = 0x14
    OUT_TEMP_L = 0x15
    OUT_TEMP_H = 0x16
    STATUS_REG = 0x17
    OUT_X_L_G = 0x18
    OUT_X_H_G = 0x19
    OUT_Y_L_G = 0x1A
    OUT_Y_H_G = 0x1B
    OUT_Z_L_G = 0x1C
    OUT_Z_H_G = 0x1D
    CTRL_REG4 = 0x1E
    CTRL_REG5_XL = 0x1F
    CTRL_REG6_XL = 0x20
    CTRL_REG7_XL = 0x21
    CTRL_REG8 = 0x22
    CTRL_REG9 = 0x23
    CTRL_REG10 = 0x24
    INT_GEN_SRC_XL = 0x26
    STATUS_REG = 0x27
    OUT_X_L_XL = 0x28
    OUT_X_H_XL = 0x29
    OUT_Y_L_XL = 0x2A
    OUT_Y_H_XL = 0x2B
    OUT_Z_L_XL = 0x2C
    OUT_Z_H_XL = 0x2D
    FIFO_CTRL = 0x2E
    FIFO_SRC = 0x2F
    INT_GEN_CFG_G = 0x30
    INT_GEN_THS_XH_G = 0x31
    INT_GEN_THS_XL_G = 0x32
    INT_GEN_THS_YH_G = 0x33
    INT_GEN_THS_YL_G = 0x34
    INT_GEN_THS_ZH_G = 0x35
    INT_GEN_THS_ZL_G = 0x36
    INT_GEN_DUR_G =  0x37

    def __init__ (self, driver = None):
        self.driver = driver

    def whoAmI (self):
        return self.driver.readReg(self.WHO_AM_I)

    def selfTest (self):
        return self.whoAmI() == self.WHO_AM_I_OK

    def readAcc (self):
        x = self.driver.readValue(self.OUT_X_L_XL, self.OUT_X_H_XL)
        y = self.driver.readValue(self.OUT_Y_L_XL, self.OUT_Y_H_XL)
        z = self.driver.readValue(self.OUT_Z_L_XL, self.OUT_Z_H_XL)
        return x, y ,z

    def readGyro (self):
        x = self.driver.readValue(self.OUT_X_L_G, self.OUT_X_H_G)
        y = self.driver.readValue(self.OUT_Y_L_G, self.OUT_Y_H_G)
        z = self.driver.readValue(self.OUT_Z_L_G, self.OUT_Z_H_G)
        return x, y, z

    def readTemp (self):
        return self.driver.readValue(self.OUT_TEMP_L, self.OUT_TEMP_H)

    def enableAcc (self):
        self.driver.writeReg(self.CTRL_REG5_XL, 0x38)
        self.driver.writeReg(self.CTRL_REG6_XL, 0x68)
        self.driver.writeReg(self.CTRL_REG7_XL, 0x00)

    def enableGyro (self):
        self.driver.writeReg(self.CTRL_REG1_G, 0xab)
        self.driver.writeReg(self.CTRL_REG4, 0x38)

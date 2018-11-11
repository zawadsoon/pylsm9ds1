#!/usr/bin/python3

import time
import queue
import threading
import asyncio
import websockets
import json

from pylsm9ds1 import ACC_GYRO
from pylsm9ds1 import MAG
from pylsm9ds1 import SMBusDriver

running = True

class AG_Thread (threading.Thread):

    def __init__ (self):
        threading.Thread.__init__(self)
        self.imu = None

    def run (self): 
        acc_driver = SMBusDriver(ACC_GYRO.ADDRESS, 1)
        mag_driver = SMBusDriver(MAG.ADDRESS, 1)
        while running is True:
            try:
                self.imu = ACC_GYRO(acc_driver)
                self.mag = MAG(mag_driver)
                self.dataLoop()
            except OSError:
                time.sleep(2)
                print("I/O Error, waiting...")
        acc_driver.close()
        mag_driver.close()

    def dataLoop (self):
        if self.imu.selfTest() is True:
            self.imu.enableGyro()
            self.imu.enableAcc()
            self.mag.enable()
            while running is True:
                gx, gy, gz = self.imu.readGyro()
                ax, ay, az = self.imu.readAcc()
                mx, my, mz = self.mag.read()
                temp = self.imu.readTemp()
                data = {
                    'acc': {'x': ax, 'y': ay, 'z': az},
                    'gyro': {'x': gx, 'y': gy, 'z': gz},
                    'mag': {'x': mx, 'y': my, 'z': mz},
                    'temp': temp
                }
                print(data)
                time.sleep(1/952)

t1 = AG_Thread()
t1.start()

while running is True:
    try:
        pass
    except KeyboardInterrupt:
        running = False
        t1.join()
        print("Bye")

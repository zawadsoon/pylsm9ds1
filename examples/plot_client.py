import sys
import time
import queue
import threading
import asyncio
import websockets
import json

sys.path.append('../')

from pylsm9ds1.acc_gyro import ACC_GYRO
from pylsm9ds1.mag import MAG
from pylsm9ds1.smbus_driver import SMBusDriver

running = True
data_queue = queue.Queue(100)

class AG_Thread (threading.Thread):

    def __init__ (self):
        threading.Thread.__init__(self)
        self.imu = None

    def run (self): 
        acc_driver = SMBusDriver(ACC_GYRO.ADDRESS)
        mag_driver = SMBusDriver(MAG.ADDRESS)
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
                data_queue.put({
                    'acc': {'x': ax, 'y': ay, 'z': az},
                    'gyro': {'x': gx, 'y': gy, 'z': gz},
                    'mag': {'x': mx, 'y': my, 'z': mz},
                    'temp': temp
                })
                time.sleep(1/952)


t1 = AG_Thread()
t1.start()

async def send_data():
    async with websockets.connect(
        'ws://192.168.1.150:8711'
    ) as ws:
        data_list = []
        for i in range(1,25):
            data_list.append(data_queue.get())

        await ws.send(
            json.dumps(data_list)
        )

loop = None

while running is True:
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            send_data()
        )
    except KeyboardInterrupt:
        loop.stop()
        running = False
        t1.join()
        print("Bye")
    except (ConnectionRefusedError, OSError):
        time.sleep(1)
        print("Retrying...")

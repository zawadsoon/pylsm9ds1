import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import asyncio
import websockets
import threading
import json

running = True

class AGPlot:
    X_LIM_L = 0
    X_LIM_H = 100
    Y_LIM_L = -4096
    Y_LIM_H = 4096

    def __init__ (self, fig, axes, y_lim_l = None, y_lim_h = None):
        self.fig = fig
        self.axes = axes
        self.x = range(1,101)
        self.y = [0] * 100
        self.line, = axes.plot(self.x, self.y)
        self.anim = animation.FuncAnimation(
            self.fig, self.animate, interval=20
        )
        if y_lim_h is None:
            y_lim_h = self.Y_LIM_H
        if y_lim_l is None:
            y_lim_l = self.Y_LIM_L
        self.axes.set_ylim(y_lim_l, y_lim_h)

    def updateY (self, newYItem):
        self.y.pop()
        self.y.insert(0, newYItem)

    def animate (self, index):
        self.line.set_ydata(self.y)

    @staticmethod
    def create(axes, name = ''):
        axes.set_ylim(AGPlot.Y_LIM_L, AGPlot.Y_LIM_H)
        axes.set_xlim(AGPlot.X_LIM_L, AGPlot.X_LIM_H)
        axes.set_ylabel(name)
        return axes

class EventLoopThread (threading.Thread):

    def __init__ (self, callback):
        threading.Thread.__init__(self)
        self.callback = callback 
        self.loop = asyncio.new_event_loop()

    def run (self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(
            websockets.serve(self.callback, '', 8711)
        )
        self.loop.run_forever()

    def join (self):
        self.loop.stop()
        super(EventLoopThread, self).join()
        
async def fetch_data (websocket, path):
    data_list = json.loads(
        await websocket.recv()
    )
    for data in data_list:
        p1.updateY(int(data.get('acc', {}).get('x')))
        p2.updateY(int(data.get('acc', {}).get('y')))
        p3.updateY(int(data.get('acc', {}).get('z')))
        p4.updateY(int(data.get('gyro', {}).get('x')))
        p5.updateY(int(data.get('gyro', {}).get('y')))
        p6.updateY(int(data.get('gyro', {}).get('z')))
        p7.updateY(int(data.get('mag', {}).get('x')))
        p8.updateY(int(data.get('mag', {}).get('y')))
        p9.updateY(int(data.get('mag', {}).get('z')))
        print(data.get('temp'))

def handle_close (event):
    running = False
    elt.join()
    print("Bye")

#Main program
fig = plt.figure()

p1 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,1), 'x'))
p2 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,4), 'y'))
p3 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,7), 'z'))

p4 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,2), 'x'), -32568, 32568)
p5 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,5), 'y'), -32568, 32568)
p6 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,8), 'z'), -32568, 32568)

p7 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,3), 'x'), -32568, 32568)
p8 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,6), 'y'), -32568, 32568)
p9 = AGPlot(fig, AGPlot.create(fig.add_subplot(3,3,9), 'z'), -32568, 32568)

elt = EventLoopThread(fetch_data)
elt.start()

fig.canvas.mpl_connect('close_event', handle_close)
plt.show()

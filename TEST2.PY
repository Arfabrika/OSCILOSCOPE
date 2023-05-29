import pyqtgraph as pg
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from pyardrone import ARDrone, at
import thread1

## Code for plot, copied form example.

## Threading and updating part

def update():
    print("update")
    update_plot_vx()
    update_plot_vy()
    update_plot_vz()


class Thread(pg.QtCore.QThread):
    newData = pg.QtCore.Signal(object)
    def run(self):
            thread1

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

thread = Thread()
thread.newData.connect(update) 
thread.start()

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
# q = {
#     1 : 1,
#     2 : 2,    
#     3 : 3,
#     4: 4,
#     5:5,
#     6:6
# }
# print()


import pyqtgraph.examples
pyqtgraph.examples.run()

from pyqtgraph.Qt import QtCore


# importing Qt widgets
from PySide6.QtWidgets import *
 
# importing system
import sys
 
# importing numpy as np
import numpy as np
 
# importing pyqtgraph as pg
import pyqtgraph as pg
from PySide6.QtGui import *
from PySide6.QtCore import *
import PySide6.QtWidgets as QtWidgets
 
"""
# Image View class
class ImageView(pg.ImageView):
 
    # constructor which inherit original
    # ImageView
    def __init__(self, *args, **kwargs):
        pg.ImageView.__init__(self, *args, **kwargs)
 
 
class Window(QMainWindow):
 
    def __init__(self):
        super().__init__()
 
        # setting title
        self.setWindowTitle("PyQtGraph")
 
        # setting geometry
        self.setGeometry(100, 100, 600, 500)
 
        # icon
        icon = QIcon("skin.png")
 
        # setting icon to the window
        self.setWindowIcon(icon)
 
        # calling method
        self.UiComponents()
 
        # showing all the widgets
        self.show()
 
    # method for components
    def UiComponents(self):
 
        # creating a widget object
        widget = QWidget()
 
        # creating a label
        label = QLabel("Geeksforgeeks Graph Item")
 
        # setting minimum width
        label.setMinimumWidth(130)
 
        # making label do word wrap
        label.setWordWrap(True)
 
        # setting configuration options
        pg.setConfigOptions(antialias=True)
 
        # creating graphics layout widget
        win = pg.GraphicsLayoutWidget()
 
        # adding view box to the graphic layout widget
        view = win.addViewBox()
 
        # lock the aspect ratio
        view.setAspectLocked()
 
        # creating a graph item
        graph_item = pg.GraphItem()
 
        # adding graph item to the view box
        view.addItem(graph_item)
 
        # Define positions of nodes
        pos = np.array([
            [0, 0],
            [10, 0],
            [0, 10],
            [10, 10],
            [5, 5],
            [15, 5]
        ])
 
        # Define the set of connections in the graph
        adj = np.array([
            [0, 1],
            [1, 3],
            [3, 2],
            [2, 0],
            [1, 5],
            [3, 5],
        ])
 
        # Define the symbol to use for each node (this is optional)
        symbols = ['o', 'x', 'o', 'o', 't', '+']
 
        # Define the line style for each connection (this is optional)
        lines = np.array([
            (255, 0, 0, 255, 1),
            (255, 0, 255, 255, 2),
            (255, 0, 255, 255, 3),
            (255, 255, 0, 255, 2),
            (255, 0, 0, 255, 1),
            (255, 255, 255, 255, 4),
        ], dtype=[('red', np.ubyte), ('green', np.ubyte), ('blue', np.ubyte), ('alpha', np.ubyte), ('width', float)])
 
        # setting data to the graph item
        graph_item.setData(pos=pos, adj=adj, pen=lines,
                           size=1, symbol=symbols, pxMode=False)
 
        # Creating a grid layout
        layout = QGridLayout()
 
        # minimum width value of the label
        label.setMinimumWidth(130)
 
        # setting this layout to the widget
        widget.setLayout(layout)
 
        # adding label in the layout
        layout.addWidget(label, 1, 0)
 
        # plot window goes on right side, spanning 3 rows
        layout.addWidget(win, 0, 1, 3, 1)
 
        # setting this widget as central widget of the main window
        self.setCentralWidget(widget)
 
 
# create pyqt5 app
if __name__ == "__main__":
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    w = Window()
    w.show()
    sys.exit(app.exec())
# import numpy as np
# x = np.random.normal(size=1000)
# y = np.random.normal(size=1000)
# pg.plot(x, y, pen=None, symbol='o')
# q = 1

""
p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='y')
data = np.random.normal(size=(10,1000))
ptr = 0
def update():
    global curve, data, ptr, p6
    curve.setData(data[ptr%10])
    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
""

""
p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='y')
data = np.random.normal(size=(10,1000))
ptr = 0
dc = {1:1, 2:2,3:3}
mas = list(dc.values())
xs = list(dc.keys())
def update():
    global curve, data, ptr, p6
    curve.setData(mas)
    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
"""
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *


class MplWidget(QWidget):
    def __init__(self, parent=QWidget):
        QWidget.__init__(self, parent)
        QWidget.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        self.canvas = FigureCanvas(Figure(figsize=(250, 130), dpi = 100))
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

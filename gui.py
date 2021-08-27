import ntpath
import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import json
import mplwidget
import os

class MyWidget(QMainWindow):

    def __init__(self):
        self.df = ''
        self.file, self.path = '', ''
        super().__init__()
        loadUi(os.getcwd() + '\line.ui', self)
        self.data = 1
        self.select_button.clicked.connect(self.loadfile)
        self.comboBox.currentIndexChanged.connect(self.select_rune_type)

    def loadfile(self):
        self.path = QFileDialog.getOpenFileName(self)[0]
        self.file = ntpath.basename(self.path)
        self.read_data()

    def read_data(self):
        f = open(self.path)

        self.data = pd.read_csv(f, sep=';')
        
        
        data = self.data['max_efficiency'].to_numpy()  # time
        data = np.sort(data)[::-1][0:250]
        self.display_line(data)
        
        # print(time)

    def display_line(self, data):
        self.mplwid.canvas.axes.clear()
        self.mplwid.canvas.axes.plot(data)
        self.mplwid.canvas.axes.grid(True)
        self.mplwid.canvas.axes.set_xlim(0,250)
        self.mplwid.canvas.axes.set_ylim(85,130)
        self.mplwid.canvas.draw()

    def select_rune_type(self):
        if (self.comboBox.currentText() == "All"):
            data = self.data['max_efficiency'].to_numpy()  # time
            data = np.sort(data)[::-1][0:250]
            self.display_line(data)
        else:
            self.display_line(self.sort_max_eff(self.data[self.data.set == self.comboBox.currentText()]))
        
    def sort_max_eff(self, data):
        data = data['max_efficiency'].to_numpy()
        data = np.sort(data)[::-1][0:250]
        return data

    def analyze(self):
        data = self.data
        data = data[data.level >= 12]
        
        maxgrinds = {"HP%":10,"DEF%":10,"ATK%":10,"HP flat":550,
                     "DEF flat":34,"ATK flat":8,"SPD":5,"RES":0, "ACC":0,
                     "CRate":0,"CDmg":0}
        maxgems = {"HP%":13,"DEF%":13,"ATK%":13,"HP flat":580,
                     "DEF flat":40,"ATK flat":40,"SPD":10,"RES":13,"ACC": 13,
                     "CRate":9,"CDmg":10}
        maxrolls = {"HP%":8,"DEF%":8,"ATK%":8,"HP flat":750,
                     "DEF flat":40,"ATK flat":40,"SPD":6,"RES":8,"ACC": 8,
                     "CRate":6,"CDmg":7}
        for i in range(0, len(data.index)):
            enchanted = False
            if (json.loads(data['s1_data'][i])["enchanted"] or json.loads(data['s2_data'][i])["enchanted"] 
                or json.loads(data['s3_data'][i])["enchanted"] or json.loads(data['s4_data'][i])["enchanted"]):
                enchanted = True

            s1 = data['s1_t'][i]
            s2 = data['s2_t'][i]
            s3 = data['s3_t'][i]
            s4 = data['s4_t'][i]

            s1_max_eff = (maxgrinds[s1] + data["s1_v"] - json.loads(data['s1_data'][i])["gvalue"]) / maxrolls[s1]
            s2_max_eff = (maxgrinds[s2] + data["s2_v"] - json.loads(data['s2_data'][i])["gvalue"]) / maxrolls[s2]
            s3_max_eff = (maxgrinds[s3] + data["s3_v"] - json.loads(data['s3_data'][i])["gvalue"]) / maxrolls[s3]
            s4_max_eff = (maxgrinds[s4] + data["s4_v"] - json.loads(data['s4_data'][i])["gvalue"]) / maxrolls[s4]
            
            max_eff = (s1_max_eff + s2_max_eff + s3_max_eff + s4_max_eff - 5) / 14
            
        
        print(json.loads(data['s1_data'][0])["enchanted"])
        
    
    
    
if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.setStyle('Fusion')
    sys.exit(app.exec_())

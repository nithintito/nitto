# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 17:30:16 2021

@author: AJOE.GEORGE
"""

from kivy_garden.graph import MeshLinePlot
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from math import sin
import pandas as pd 

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__()
        self.plot = MeshLinePlot(color=[.5, .5, 1, 1])
        self.plot1 = MeshLinePlot(color=[.5, .5, 1, 1])
        self.plot2 = MeshLinePlot(color=[.5, .5, 1, 1])

    def start(self):
            data_to_graph=pd.read_csv('Pressure.csv')
           # dat=pd.read_csv('Pressure.csv') 
            self.plot.points =  list(data_to_graph.itertuples(index=False))
            self.plot1.points =  list(data_to_graph.itertuples(index=False))
            self.plot2.points =  list(data_to_graph.itertuples(index=False))               
            self.ids.graph.add_plot(self.plot)
            self.ids.graph2.add_plot(self.plot1)
            self.ids.graph3.add_plot(self.plot2)            

class Engine_Analyser(App):
    def build(self):
        return Builder.load_file("mainWindow_play.kv")

if __name__ == "__main__":
    Engine_Analyser().run()

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.widget import Widget

#file manager
from kivy.uix.filechooser import FileChooserIconView
import os
from kivy.lang import Builder

import numpy as np
import time

Builder.load_string('''
<MyWidget>:
    cols:2
    id:my_widget

    FileChooserIconView:
        id:filechooser
        on_selection: my_widget.selected(filechooser.selection)
''')

class MyWidget(GridLayout):
    def selected(self, filename):
        try:
            matrix = np.load(filename[0], allow_pickle=True)
            np.save('matrix0', matrix)
            time.sleep(0.5)
            os.startfile('main2.py')
            #os.system("TASKKILL /F /IM python.exe")#3drb1.exe и себя
        except:
            pass

class TestApp(App):
    def build(self):
        return MyWidget()


if __name__ == "__main__":
    TestApp().run()

# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import StringProperty

import sys
sys.path.append('..')
from Tools import makeqr

class TestWidget(Widget):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(TestWidget, self).__init__(**kwargs)
        self.text = 'This is Wartermarking Demo App.'

    def buttonClicked(self):
        self.text = 'Embed'

    def buttonClicked2(self):
        self.text = 'Show'

    def buttonClicked3(self):
        self.text = 'Extract'


class WatermarkDemoApp(App):
    def __init__(self, **kwargs):
        super(WatermarkDemoApp, self).__init__(**kwargs)
        self.title = 'WatermarkDemoApp'

if __name__ == '__main__':
    WatermarkDemoApp().run()

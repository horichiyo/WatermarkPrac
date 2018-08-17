# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.modalview import ModalView

# デフォルトに使用するフォントを変更する
resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

import sys
sys.path.append('..')
from Tools import makeqr

class TestWidget(Widget):
    text = StringProperty()
    image_src =StringProperty()

    def __init__(self, **kwargs):
        super(TestWidget, self).__init__(**kwargs)
        self.text = 'This is Wartermarking Demo App.ああ'
        self.image_src = '../Images/lena256.bmp'

    def buttonClicked(self):
        self.text = 'Embed'

    def buttonClicked2(self):
        self.text = 'Show'

    def buttonClicked3(self):
        self.text = 'Extract'

    def descriptionButtonClicked(self):
        descriptionView = DescriptionView()
        descriptionView.open()


class DescriptionView(ModalView):
    def __init__(self, **kwargs):
        super(DescriptionView, self).__init__(**kwargs)

    def clearButtonClicked(self):
        self.dismiss()


class WatermarkDemoApp(App):
    def __init__(self, **kwargs):
        super(WatermarkDemoApp, self).__init__(**kwargs)
        self.title = 'WatermarkDemoApp'

if __name__ == '__main__':
    WatermarkDemoApp().run()

# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.modalview import ModalView

from PIL import Image
import sys
sys.path.append('..')
from Tools import makeqr
from watermarking import imageInImageWatermarking

# デフォルトに使用するフォントを変更する
resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')


class AppWidget(Widget):
    text = StringProperty()
    cover_image_src =StringProperty()
    stego_image_src =StringProperty()
    embed_message = StringProperty()
    extract_message = StringProperty()


    def __init__(self, **kwargs):
        super(AppWidget, self).__init__(**kwargs)
        self.extract_message = '抽出した文字はここに表示されます。'
        self.cover_image_src = '../Images/lena256.bmp'
        self.stego_image_src = '../Images/result/stego_fft.bmp'

    def embedButtonClicked(self):
        self.text = 'Embed'
        self.embed_message =  self.ids["text_box"].text
        imageInImageWatermarking.embedQrcodeUseFFT(self.embed_message)


    def extractButtonClicked(self):
        extractMessageView = ExtractMessageView()
        self.text = 'Extract'
        # self.extract_message = imageInImageWatermarking.decodeQrcode('fft')
        extractMessageView.open()

    def descriptionButtonClicked(self):
        descriptionView = DescriptionView()
        descriptionView.open()


class DescriptionView(ModalView):
    def __init__(self, **kwargs):
        super(DescriptionView, self).__init__(**kwargs)

    def clearButtonClicked(self):
        self.dismiss()


class ExtractMessageView(ModalView):
    extract_message = StringProperty()
    def __init__(self, **kwargs):
        super(ExtractMessageView, self).__init__(**kwargs)
        self.extract_message = imageInImageWatermarking.decodeQrcode('fft')


    def clearButtonClicked(self):
        self.dismiss()


class WatermarkDemoApp(App):
    def __init__(self, **kwargs):
        super(WatermarkDemoApp, self).__init__(**kwargs)
        self.title = 'WatermarkDemoApp'

if __name__ == '__main__':
    WatermarkDemoApp().run()

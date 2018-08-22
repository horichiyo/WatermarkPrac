# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import os
from PIL import Image
import sys
sys.path.append('..')
from Tools import makeqr
from watermarking import imageInImageWatermarking as iw

# デフォルトに使用するフォントを変更する
resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')


class AppWidget(Widget):
    text = StringProperty()
    cover_image_src =StringProperty()
    cover_image_path =StringProperty()
    stego_image_src =StringProperty()
    embed_message = StringProperty()
    extract_message = StringProperty()
    psnr = StringProperty()
    mode = StringProperty()
    file_path = StringProperty()

    def __init__(self, **kwargs):
        super(AppWidget, self).__init__(**kwargs)
        self.extract_message = '抽出した文字はここに表示されます。'
        self.cover_image_src = 'lena256.bmp'
        self.cover_image_path = '../images/lena256.bmp'
        self.stego_image_src = '../Images/stegosaurus.png'
        self.psnr = ''
        self.mode = 'FFT'

    def embedButtonClicked(self):
        self.text = 'Embed'
        self.embed_message =  self.ids["text_box"].text

        if self.mode == 'FFT':
            iw.embedQrcodeUseFFT(self.embed_message, cover=self.cover_image_src)
            self.stego_image_src = '../images/result/stego_fft.bmp'
            Clock.schedule_interval(self.update, 0.01)
        elif self.mode == 'DWT':
            iw.embedQrcodeUseDWT(self.embed_message, cover=self.cover_image_src)
            self.stego_image_src = '../images/result/stego_dwt.bmp'
            Clock.schedule_interval(self.update, 0.01)

    def update(self, dt):
        self.ids['img1'].reload()

    def extractButtonClicked(self):
        extractMessageView = ExtractMessageView()
        self.text = 'Extract'
        self.psnr = str(iw.psnr('../Images/'+self.cover_image_src, self.stego_image_src))

        extractMessageView.open()

    def changeButtonClicked(self):
        content = PopupChooseFile(select=self.selectFile, cancel=self.cancelButtonClicked)
        self.popup = Popup(title="Select Image file", content=content)
        self.popup.open()

    def selectFile(self, file_path):
        self.cover_image_src = os.path.basename(file_path)
        self.cover_image_path= '../images/'+os.path.basename(file_path)
        self.popup.dismiss()

    def cancelButtonClicked(self):
        self.popup.dismiss()
        # self.info.text = 'Cancel'

    def modeButtonClicked(self):
        content = ModeSelectPopUp(fft=self.useFFT, dwt=self.useDWT, text='You can select the method to use for watermarking.')
        self.popup = Popup(title="Mode Select", content=content)
        self.popup.open()

    def useFFT(self):
        self.mode = 'FFT'
        self.popup.dismiss()

    def useDWT(self):
        self.mode = 'DWT'
        self.popup.dismiss()


class ExtractMessageView(ModalView):
    extract_message = StringProperty()

    def __init__(self, **kwargs):
        super(ExtractMessageView, self).__init__(**kwargs)
        self.extract_message = iw.decodeQrcode()

    def clearButtonClicked(self):
        self.dismiss()


class ModeSelectPopUp(BoxLayout):
    text = StringProperty()
    fft  = ObjectProperty()
    dwt  = ObjectProperty()


class PopupChooseFile(BoxLayout):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    joined_path = os.path.join(current_dir, '../images/')
    target_path = os.path.normpath(joined_path)
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class WatermarkDemoApp(App):
    def __init__(self, **kwargs):
        super(WatermarkDemoApp, self).__init__(**kwargs)
        self.title = 'WatermarkDemoApp'


if __name__ == '__main__':
    WatermarkDemoApp().run()

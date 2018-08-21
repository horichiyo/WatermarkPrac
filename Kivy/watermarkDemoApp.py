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
    stego_image_src =StringProperty()
    embed_message = StringProperty()
    extract_message = StringProperty()
    psnr = StringProperty()
    mode = StringProperty()

    def __init__(self, **kwargs):
        super(AppWidget, self).__init__(**kwargs)
        self.extract_message = '抽出した文字はここに表示されます。'
        self.cover_image_src = '../Images/lena256.bmp'
        self.stego_image_src = '../Images/stegosaurus.png'
        self.psnr = ''
        self.mode = 'FFT'

    def embedButtonClicked(self):
        self.text = 'Embed'
        self.embed_message =  self.ids["text_box"].text

        if self.mode == 'FFT':
            iw.embedQrcodeUseFFT(self.embed_message)
            self.stego_image_src = '../Images/result/stego_fft.bmp'
        elif self.mode == 'DWT':
            iw.embedQrcodeUseDWT(self.embed_message)
            self.stego_image_src = '../Images/result/stego_dwt.bmp'

    def extractButtonClicked(self):
        extractMessageView = ExtractMessageView()
        self.text = 'Extract'
        self.psnr = str(iw.psnr(self.cover_image_src, self.stego_image_src))

        extractMessageView.open()

    def manualButtonClicked(self):
        modeView = ModeView()
        modeView.open()

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


class ManualView(ModalView):
    def __init__(self, **kwargs):
        super(ManualView, self).__init__(**kwargs)

    def clearButtonClicked(self):
        self.dismiss()


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


class WatermarkDemoApp(App):
    def __init__(self, **kwargs):
        super(WatermarkDemoApp, self).__init__(**kwargs)
        self.title = 'WatermarkDemoApp'


if __name__ == '__main__':
    WatermarkDemoApp().run()

# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from DiscreteWaveletTransform import dwt
from Tools import makeqr
import pywt
import cv2
import numpy as np
from PIL import Image

imgPath    = '../images/'
outImgPath = '../images/result/'
wavelet    = 'haar'  # wavelist.txtにどれを指定できるか書いてある
level      = 1


def DWT_gray(coverImageName, watermarkImageName, save=False):
    coverImage = cv2.imread(imgPath+coverImageName)
    watermarkImage = cv2.imread(imgPath+watermarkImageName)
    watermarkImage = cv2.resize(watermarkImage, (int(len(coverImage)/2), int(len(coverImage)/2)))

    # _show(cv2.imread(imgPath+coverImageName), title='Cover Image')
    # _show(cv2.imread(imgPath+watermarkImageName), title='Watermark Image')

    # DWT on cover image
    coverImage_ycc = cv2.cvtColor(coverImage, cv2.COLOR_BGR2YCR_CB)
    coverImage_y = coverImage_ycc[:,:,0]
    coverImage_y = np.float64(coverImage_y)
    coeffC = pywt.dwt2(coverImage_y, wavelet)
    cA, (cH, cV, cD) = coeffC

    watermarkImage_ycc = cv2.cvtColor(watermarkImage, cv2.COLOR_BGR2YCR_CB)
    watermarkImage_y = watermarkImage_ycc[:,:,0]
    watermarkImage_y = watermarkImage_y.astype(np.float64)

    # Embedding
    coeffW = cA, (cH, cV, 0.4*cD+0.1*watermarkImage_y)

    watermarkedImage = pywt.idwt2(coeffW, wavelet)
    _show(watermarkedImage, title='Watermarked Image')

    # Extraction
    coeffWM = pywt.dwt2(watermarkedImage, wavelet)
    hA, (hH, hV, hD) = coeffWM

    extracted = (hD - 0.4*cD) / 0.1
    extracted = np.uint8(extracted)

    _show(extracted, title='Extracted Image')

    if save == True:
        Image.fromarray(extracted).save(outImgPath + 'extract_dwt.bmp')


def DWT_color(coverImageName, watermarkImageName):
    pass
    # coverImage = cv2.imread(imgPath+coverImageName)
    # watermarkImage = cv2.imread(imgPath+watermarkImageName)
    # watermarkImage = cv2.resize(watermarkImage, (int(len(coverImage)/2), int(len(coverImage)/2)))
    #
    # # _show(cv2.imread(imgPath+coverImageName), title='Cover Image')
    # # _show(cv2.imread(imgPath+watermarkImageName), title='Watermark Image')
    #
    # # DWT on cover image
    # coverImage_ycc = cv2.cvtColor(coverImage, cv2.COLOR_BGR2YCR_CB)
    #
    # coverImage_y = coverImage_ycc[:, :, 0]
    # coverImage_y = np.float64(coverImage_y)
    # # coverImage_y /= 255
    # coeffC_y = pywt.dwt2(coverImage_y, wavelet)
    # cA_y, (cH_y, cV_y, cD_y) = coeffC_y
    #
    # coverImage_cr = coverImage_ycc[:, :, 1]
    # coverImage_cr = np.float64(coverImage_cr)
    # # coverImage_cr /= 255
    # coeffC_cr = pywt.dwt2(coverImage_cr, wavelet)
    # cA_cr, (cH_cr, cV_cr, cD_cr) = coeffC_cr
    #
    # coverImage_cb = coverImage_ycc[:, :, 2]
    # coverImage_cb = np.float64(coverImage_cb)
    # # coverImage_cb /= 255
    # coeffC_cb = pywt.dwt2(coverImage_cb, wavelet)
    # cA_cb, (cH_cb, cV_cb, cD_cb) = coeffC_cb
    #
    #
    # watermarkImage_ycc = cv2.cvtColor(watermarkImage, cv2.COLOR_BGR2YCR_CB)
    #
    # watermarkImage_y = watermarkImage_ycc[:, :, 0]
    # watermarkImage_y = watermarkImage_y.astype(np.float64)
    # # watermarkImage_y /= 255
    #
    # watermarkImage_cr = watermarkImage_ycc[:, :, 1]
    # watermarkImage_cr = watermarkImage_cr.astype(np.float64)
    # # watermarkImage_cr /= 255
    #
    # watermarkImage_ycc = cv2.cvtColor(watermarkImage, cv2.COLOR_BGR2YCR_CB)
    # watermarkImage_cb = watermarkImage_ycc[:, :, 2]
    # watermarkImage_cb = watermarkImage_cb.astype(np.float64)
    # # watermarkImage_cb /= 255
    #
    #
    # # Embedding
    #
    # coeffW_y = cA_y, (cH_y, cV_y, 0.4*cD_y+0.1*watermarkImage_y)
    # coeffW_cr = cA_cr, (cH_cb, cV_cr, 0.4*cD_cr+0.1*watermarkImage_cr)
    # coeffW_cb = cA_cb, (cH_cb, cV_cb, 0.4 * cD_cb + 0.1 * watermarkImage_cb)
    #
    # watermarkedImage_y = pywt.idwt2(coeffW_y, wavelet)
    # watermarkedImage_cr = pywt.idwt2(coeffW_cr, wavelet)
    # watermarkedImage_cb = pywt.idwt2(coeffW_cb, wavelet)
    #
    # watermarkedImage_ycc = np.dstack([watermarkedImage_y, watermarkedImage_cr, watermarkedImage_cb])
    # print(coverImage)
    # watermarkedImage_ycc = np.uint8(watermarkedImage_ycc)
    # print('------')
    # watermarkedImage_bgr = cv2.cvtColor(watermarkedImage_ycc, cv2.COLOR_BGR2YCR_CB)
    # print(watermarkedImage_bgr)
    #
    # # _show(watermarkedImage_bgr, title='Watermarked Image')
    # return
    #
    # # Extraction
    # # coeffWM = pywt.dwt2(watermarkedImage, wavelet)
    # # hA, (hH, hV, hD) = coeffWM
    #
    # # extracted = (hD - 0.4*cD) / 0.1
    # # extracted *= 255
    # # extracted = np.uint8(extracted)
    # #
    # # _show(extracted, title='Extracted')
    #
    # # y = (hD - 0.4*cD) / 0.1
    # # y *= 255
    # # y = np.uint8(y)
    # # b = (hV - 0.4*cV) / 0.1
    # # b*=255
    # # b = np.uint8(b)
    # # r = (hH - 0.4*cV) / 0.1
    # # r*=255
    # # r = np.uint8(r)
    # # dwt.saveYcbcrAsImg('lake_out.bmp', y, r, b)


def FFT(coverImageName, watermarkImageName, save=False):
    coverImage = cv2.imread(imgPath + coverImageName)
    watermarkImage = cv2.imread(imgPath + watermarkImageName)
    watermarkImage = cv2.resize(watermarkImage, (int(len(coverImage)), int(len(coverImage))))

    _show(coverImage, title='Cover Image')
    _show(watermarkImage, title='watermarkImage')

    # embed
    watermarkedImage = _calcFFT(coverImage, watermarkImage, 0.1)

    _show(watermarkedImage, 'Watermarked Image')

    # extract
    extractImage = _calcIFFT(coverImage, watermarkedImage, 0.1)

    _show(extractImage, 'Extract Image')

    if (save==True):
        Image.fromarray(np.uint8(extractImage)).save(outImgPath + 'extract_fft.bmp')


def _calcFFT(coverMat, watermarkMat, strength):
    shiftedFFT = np.fft.fftshift(np.fft.fft2(coverMat))
    watermarkedFFT = shiftedFFT + strength*watermarkMat
    watermarkedImage = np.fft.ifft2(np.fft.ifftshift(watermarkedFFT))

    return watermarkedImage

def _calcIFFT(coverMat, watermarkedMat, strength):
    shiftedFFT_watermarked = np.fft.fftshift(np.fft.fft2(watermarkedMat))
    shiftedFFT_cover = np.fft.fftshift(np.fft.fft2(coverMat))
    extractMat = np.abs(shiftedFFT_watermarked - shiftedFFT_cover) / strength
    # extractMat = np.abs(shiftedFFT_cover-shiftedFFT_watermarked) / strength
    extractImage = extractMat

    return extractImage

def _saveGrayImg(imgName):
    img = np.array(Image.open(imgPath+imgName), 'f')
    gray_img = Image.fromarray(np.uint8(img)).convert('L')
    gray_img.save(outImgPath+'gray'+imgName)

def _show(img,title='title'):

    img_s = np.uint8(img.real)
    img_resize = cv2.resize(img_s, (512, 512))
    cv2.WINDOW_NORMAL
    cv2.imshow(title, img_resize)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def _embedQrcodeUseFFT(message):
    qr = makeqr.generateQrcode(message)
    qr = makeqr.qrsizeChange(qr)
    Image.fromarray(qr).save(imgPath + 'QR.bmp')
    FFT('lena256.bmp', 'QR.bmp', save=True)

def _embedQrcodeUseDwt(message):
    qr = makeqr.generateQrcode(message)
    qr = makeqr.qrsizeChange(qr)
    Image.fromarray(qr).save(imgPath + 'QR.bmp')
    DWT_gray('lena512.bmp', 'QR.bmp', save=True)

def _decodeQrcode():
    qr = cv2.imread(outImgPath + 'extract_dwt.bmp')
    return makeqr.decodeQrcode(np.uint8(qr))


def main():
    _embedQrcodeUseDwt('最大で400文字ちょい埋め込むことができます。')
    print(_decodeQrcode())

if __name__ == '__main__':
    main()



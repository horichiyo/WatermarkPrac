# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from Tools import makeqr
import pywt
import cv2
import math
import numpy as np
from PIL import Image

imgPath    = '../images/'
outImgPath = '../images/result/'
wavelet    = 'haar'  # wavelist.txtにどれを指定できるか書いてある
level      = 1


def embedQrcodeUseFFT(message, cover='lena512.bmp'):
    qr = makeqr.generateQrcode(message)
    qr = makeqr.qrsizeChange(qr)
    Image.fromarray(qr).save(imgPath + 'QR.bmp')
    _FFT(cover, 'QR.bmp', save=True)

def embedQrcodeUseDWT(message, cover='lena512.bmp'):
    qr = makeqr.generateQrcode(message)
    qr = makeqr.qrsizeChange(qr)
    Image.fromarray(qr).save(imgPath + 'QR.bmp')
    _DWT_color(cover, 'QR.bmp', save=True)

def decodeQrcode():
    qr = cv2.imread(outImgPath + 'extract.bmp')
    return makeqr.decodeQrcode(np.uint8(qr))

def psnr(cover, stego):
    coverImg = np.array(Image.open(cover), 'f')
    stegoImg = np.array(Image.open(stego), 'f')
    if coverImg.shape != stegoImg.shape:
        return '?'
    mse = np.mean((coverImg-stegoImg)**2)
    if mse == 0:
        return math.inf
    PIXEL_MAX = 255.0
    return round(20 * math.log10(PIXEL_MAX/math.sqrt(mse)), 3)

def _DWT_gray(coverImageName, watermarkImageName, save=False):
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
    # _show(watermarkedImage, title='Watermarked Image')

    # Extraction
    coeffWM = pywt.dwt2(watermarkedImage, wavelet)
    hA, (hH, hV, hD) = coeffWM

    extracted = (hD - 0.4*cD) / 0.1
    extracted = np.uint8(extracted)

    # _show(extracted, title='Extracted Image')

    if save == True:
        Image.fromarray(extracted).save(outImgPath + 'extract.bmp')

def _DWT_color(coverImageName, watermarkImageName, save=False):
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
        coverImage_ycc[:,:,0] = watermarkedImage
        stego_bgr = cv2.cvtColor(coverImage_ycc, cv2.COLOR_YCrCb2BGR)
        cv2.imwrite(outImgPath + 'stego_dwt.bmp', stego_bgr)

        # Extraction
        coeffWM = pywt.dwt2(watermarkedImage, wavelet)
        hA, (hH, hV, hD) = coeffWM

        extracted = (hD - 0.4*cD) / 0.1
        extracted = np.uint8(extracted)

        # _show(extracted, title='Extracted Image')

        if save == True:
            Image.fromarray(extracted).save(outImgPath + 'extract.bmp')

def _FFT(coverImageName, watermarkImageName, save=False):
    coverImage = cv2.imread(imgPath + coverImageName)
    watermarkImage = cv2.imread(imgPath + watermarkImageName)
    watermarkImage = cv2.resize(watermarkImage, (int(len(coverImage)), int(len(coverImage))))

    # _show(coverImage, title='Cover Image')
    # _show(watermarkImage, title='watermarkImage')

    # embed
    watermarkedImage = _calcFFT(coverImage, watermarkImage, 0.1)
    # BGR -> RGBに変換
    watermarkedImage_rgb = watermarkedImage[:, :, ::-1].copy()
    Image.fromarray(np.uint8(watermarkedImage_rgb.real)).save(outImgPath + 'stego_fft.bmp')

    # _show(watermarkedImage, 'Watermarked Image')

    # extract
    extractImage = _calcIFFT(coverImage, watermarkedImage, 0.1)

    # _show(extractImage, 'Extract Image')

    if (save==True):
        # BGR -> RGBに変換
        extractImage_rgb = extractImage[:, :, ::-1].copy()
        Image.fromarray(np.uint8(extractImage_rgb)).save(outImgPath + 'extract.bmp')

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

def main():
    embedQrcodeUseDWT('最大で400文字ぐらい埋め込むことができます。')
    print(decodeQrcode())


if __name__ == '__main__':
    main()

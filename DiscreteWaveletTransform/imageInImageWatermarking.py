import dwt
import pywt
import cv2
import numpy as np
from PIL import Image

imgPath    = '../images/'
outImgPath = '../images/result/'
wavelet    = 'haar'  # wavelist.txtにどれを指定できるか書いてある
level      = 1


def DWT_gray(coverImageName, watermarkImageName):
    coverImage = np.array(Image.open(imgPath+coverImageName), 'f')
    watermarkImage = np.array(Image.open(imgPath+watermarkImageName), 'f')
    watermarkImage = cv2.resize(watermarkImage, (int(len(coverImage)/2), int(len(coverImage)/2)))

    # _show(cv2.imread(imgPath+coverImageName), title='Cover Image')
    # _show(cv2.imread(imgPath+watermarkImageName), title='Watermark Image')

    # DWT on cover image
    coverImage_ycc = cv2.cvtColor(coverImage, cv2.COLOR_BGR2YCR_CB)
    coverImage_y = coverImage_ycc[:,:,0]
    coverImage_y = np.float64(coverImage_y)
    coverImage /= 255
    coeffC = pywt.dwt2(coverImage_y, wavelet)
    cA, (cH, cV, cD) = coeffC

    watermarkImage_ycc = cv2.cvtColor(watermarkImage, cv2.COLOR_BGR2YCR_CB)
    watermarkImage_y = watermarkImage_ycc[:,:,0]
    watermarkImage_y = watermarkImage_y.astype(np.float64)
    watermarkImage_y /= 255

    # Embedding
    coeffW = cA, (cH, cV, 0.4*cD+0.1*watermarkImage_y)

    watermarkedImage = pywt.idwt2(coeffW, wavelet)
    _show(watermarkedImage, title='Watermarked Image')

    # Extraction
    coeffWM = pywt.dwt2(watermarkedImage, wavelet)
    hA, (hH, hV, hD) = coeffWM

    extracted = (hD - 0.4*cD) / 0.1
    extracted *= 255
    extracted = np.uint8(extracted)

    _show(extracted, title='Extracted')


def DWT_color(coverImageName, watermarkImageName):
    coverImage = np.array(Image.open(imgPath+coverImageName), 'f')
    watermarkImage = np.array(Image.open(imgPath+watermarkImageName), 'f')
    watermarkImage = cv2.resize(watermarkImage, (int(len(coverImage)/2), int(len(coverImage)/2)))

    # _show(cv2.imread(imgPath+coverImageName), title='Cover Image')
    # _show(cv2.imread(imgPath+watermarkImageName), title='Watermark Image')

    # DWT on cover image
    coverImage = np.float64(coverImage)
    coverImage /= 255
    coeffC = pywt.dwt2(coverImage, wavelet)
    cA, (cH, cV, cD) = coeffC

    # TODO:上のを使って読み込むやつ作成
    _, _, watermarkImage, cr, cb = dwt.getImgSizeAndData(watermarkImageName)
    watermarkImage = watermarkImage.astype(np.float64)
    watermarkImage /= 255

    cr = cr.astype(np.float64)
    cr /= 255
    cb = cb.astype(np.float64)
    cb /= 255

    # Embedding
    # coeffW = cA, (cH, cV, 0.4*cD+0.1*watermarkImage)
    coeffW = cA, (cH*0.4+0.1*cr, cV*0.4+0.1*cb, 0.4*cD+0.1*watermarkImage)

    watermarkedImage = pywt.idwt2(coeffW, wavelet)
    _show(watermarkedImage, title='Watermarked Image')

    # Extraction
    coeffWM = pywt.dwt2(watermarkedImage, wavelet)
    hA, (hH, hV, hD) = coeffWM

    # extracted = (hD - 0.4*cD) / 0.1
    # extracted *= 255
    # extracted = np.uint8(extracted)
    #
    # _show(extracted, title='Extracted')

    y = (hD - 0.4*cD) / 0.1
    y *= 255
    y = np.uint8(y)
    b = (hV - 0.4*cV) / 0.1
    b*=255
    b = np.uint8(b)
    r = (hH - 0.4*cV) / 0.1
    r*=255
    r = np.uint8(r)
    dwt.saveYcbcrAsImg('lake_out.bmp', y, r, b)


def _saveGrayImg(imgName):
    img = np.array(Image.open(imgPath+imgName), 'f')
    gray_img = Image.fromarray(np.uint8(img)).convert('L')
    gray_img.save(outImgPath+'gray'+imgName)

def _show(img,title='title'):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    DWT_gray('lena512.bmp', 'lake.bmp')

if __name__ == '__main__':
    # https://goo.gl/forms/D0ioYIAt0gpwYyGO2
    main()



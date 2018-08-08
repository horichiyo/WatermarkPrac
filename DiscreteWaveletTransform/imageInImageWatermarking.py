import dwt
import pywt
import cv2
import numpy as np
from PIL import Image

imgPath    = '../images/'
outImgPath = '../images/result/'
wavelet    = 'haar'  # wavelist.txtにどれを指定できるか書いてある
level      = 1


def DWT(coverImageName, watermarkImageName):
    coverImage = np.array(Image.open(imgPath+coverImageName), 'f')
    watermarkImage = np.array(Image.open(imgPath+watermarkImageName), 'f')


    coverImage = cv2.resize(coverImage, (512, 512))
    cv2.imshow('Cover Image', cv2.imread(imgPath+coverImageName))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    watermarkImage = cv2.resize(watermarkImage, (256, 256))
    cv2.imshow('Watermark Image', cv2.imread(imgPath+watermarkImageName))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # DWT on cover image
    coverImage = np.float64(coverImage)
    coverImage /= 255
    coeffC = pywt.dwt2(coverImage, 'haar')
    cA, (cH, cV, cD) = coeffC

    _, _, watermarkImage, _, _ = dwt.getImgSizeAndData(watermarkImageName)
    watermarkImage = watermarkImage.astype(np.float64)
    watermarkImage /= 255

    # Embedding
    coeffW = (0.4 * cA + 0.1 * watermarkImage, (cH, cV, cD))
    watermarkedImage = pywt.idwt2(coeffW, 'haar')
    cv2.imshow('Watermarked Image', watermarkedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Extraction
    coeffWM = pywt.dwt2(watermarkedImage, 'haar')
    hA, (hH, hV, hD) = coeffWM

    extracted = (hA - 0.4 * cA) / 0.1
    extracted *= 255;
    extracted = np.uint8(extracted)
    cv2.imshow('Extracted', extracted)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def _saveGrayImg(imgName):
    img = np.array(Image.open(imgPath+imgName), 'f')
    gray_img = Image.fromarray(np.uint8(img)).convert('L')
    gray_img.save(outImgPath+'gray'+imgName)


def main():
    DWT('graylena512.bmp', 'lake.bmp')

if __name__ == '__main__':
    # https://goo.gl/forms/D0ioYIAt0gpwYyGO2
    main()



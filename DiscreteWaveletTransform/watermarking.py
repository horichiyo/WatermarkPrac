import pywt
import numpy as np
from PIL import Image
import dwt
import sys


outImgPath = '../images/result/'
imgPath    = '../images/'
imgName    = 'lena512.bmp'
# imgName    = 'dwt_resultlena512.bmp'
wavelet    = 'db1'  # wavelist.txtにどれを指定できるか書いてある
level      = 1


def embedBitreplaceUsingDwt(secretData, imgName=imgName):
    width, height, img_y, img_cr, img_cb = dwt.getImgSizeAndData(imgName)
    coeffs = pywt.dwt2(img_y, wavelet=wavelet)
    cA, (cH, cV, cD) = coeffs
    # Watermarking area
    if (height/2) * (width/2) < len(secretData):
        print('Secret information is over the limit of embeded.')
        print('Please review the cover image, secret information or interval.')
        sys.exit()

    cover = cD.flatten()
    stego = cover

    for i, secret_bit in enumerate(secretData):
        stego[i] = _addBitToData(cover[i], secret_bit)

    stego = np.reshape(stego, (int(height/2), int(width/2)))

    coeffs_r = cA, (cH, cV, stego)
    img_y_f = pywt.waverec2(coeffs_r, wavelet=wavelet)
    dwt.saveYcbcrAsImg('dwt_result'+imgName, img_y_f, img_cr, img_cb)


def extractBitReplaceUsingDwt():
    pass

def _addBitToData(cover, secretBit):
    stego = int(round(cover))
    stego = format(stego, '08b')
    stego = stego[::-1]

    if secretBit == 0:
        if stego[0] == '0':
            pass
        elif stego[0] == '1':
            stego = stego[:(0)] + '0' + stego[1:]
    elif secretBit == 1:
        if stego[0] == '0':
            stego = stego[:0] + '1' + stego[1:]
        elif stego[0] == '1':
            pass

    stego = stego[::-1]
    stego = int(stego, 2)
    return stego

def _extractAllDataForDwt():
    pass

def calcBer(resultData, rightData):
    if len(resultData) != len(rightData):
        print('配列の長さが違います')
        sys.exit()

    tmp = resultData - rightData

    print(resultData)
    print(rightData)
    print(tmp)

    return np.count_nonzero(tmp)/len(rightData)



def main():
    secretData = np.array([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1])
    embedBitreplaceUsingDwt(secretData, imgName=imgName)


if __name__ == '__main__':
    main()
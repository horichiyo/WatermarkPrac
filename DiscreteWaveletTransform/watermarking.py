import pywt
import numpy as np
from PIL import Image
import dwt
import sys


outImgPath     = '../images/result/'
imgPath        = '../images/'
embedImgName   = 'balls.jpg'
extractImgName = 'embed_dwt_'+embedImgName
wavelet        = 'db1'  # wavelist.txtにどれを指定できるか書いてある
level          = 1


def embedBitreplaceForDwt(secretData, imgName=embedImgName):
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

    coeffs_r = cA, (cH, cV, np.array(stego, dtype=np.int64))
    img_y_f = pywt.waverec2(coeffs_r, wavelet=wavelet)

    dwt.saveYcbcrAsImg('embed_dwt_'+imgName, img_y_f, img_cr, img_cb)


def extractBitReplaceForDwt(secretDataLength, stegoImgName=outImgPath+extractImgName, coverImgName=embedImgName):
    width_stg, height_stg, img_y_stg, img_cr_stg, img_cb_stg = dwt.getImgSizeAndData(stegoImgName)
    coeffs_stg = pywt.dwt2(img_y_stg, wavelet=wavelet)
    cA_stg, (cH_stg, cV_stg, cD_stg) = coeffs_stg
    stego = cD_stg.flatten()

    width_cvr, height_cvr, img_y_cvr, img_cr_cvr, img_cb_cvr = dwt.getImgSizeAndData(stegoImgName)
    coeffs_cvr = pywt.dwt2(img_y_cvr, wavelet=wavelet)
    cA_cvr, (cH_cvr, cV_cvr, cD_cvr) = coeffs_cvr
    cover = cD_cvr.flatten()

    secretData = np.zeros(secretDataLength)

    for i in range(secretDataLength):
        secretData[i] = _extractAllDataForDwt(stego[i])

    return secretData


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

def _extractAllDataForDwt(stego):
    stego = float('{:.3f}'.format(stego))
    stego = int(round(stego))
    stego = format(stego, '08b')
    stego = stego[::-1]

    if stego[0] == '0':
        return 0
    elif stego[0] == '1':
        return 1

def calcBer(resultData, rightData):
    if len(resultData) != len(rightData):
        print('配列の長さが違います')
        sys.exit()

    tmp = resultData - rightData

    print(resultData)
    print(rightData)

    return np.count_nonzero(tmp)/len(rightData)

def dwtBitreplaceWatermark():
    secretData = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    embedBitreplaceForDwt(secretData, imgName=embedImgName)
    result = extractBitReplaceForDwt(secretData.size)
    print(calcBer(secretData, result))

def dataToBin(data):
    bin = []
    for i in data:
        data_t = int(format(ord(i),'b'))
        bin.append('{0:021d}'.format(data_t))
    return  bin

def binToData(bin):
    data = []
    for i in bin:
        data.append(chr(int(i, 2)))
    return data


def main():
    # print(ord('あ'), chr(12354))
    tmp = ["あ","＄","!","0","]","|","/","堀"]
    bin = dataToBin(tmp)
    print(bin)
    print(binToData(bin))

if __name__ == '__main__':
    main()
import qrcode
import zbarlight
import numpy as np
from PIL import Image


def boolToInt(array):
    return np.where(array == True, 255, 0)

def generateQrcode(data, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=5, border=4):
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data=data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    print('Pixel size is '+str(img.pixel_size)+'.')

    return boolToInt(np.array(img))

def decodeQrcode(data):
    qrImg = Image.fromarray(np.uint8(data))
    codes = zbarlight.scan_codes('qrcode', qrImg)
    for i in codes:
        codes = i.decode('utf-8', 'ignore')

    return codes

def qrsizeChange(array):
    next_pow2 =  int(np.log2(2 ** np.ceil(np.log2(len(array)))))
    return np.asarray(Image.fromarray(np.uint8(array)).resize((int(2**next_pow2), int(2**next_pow2))))

def main():
    # encode
    tmp = generateQrcode('私はオーストラリアでInternshipをしています！')
    # decode
    tmp_a = qrsizeChange(tmp)
    print(decodeQrcode(tmp_a))



if __name__ == '__main__':
    main()
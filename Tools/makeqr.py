import qrcode
import math
import zbarlight
import numpy as np
from PIL import Image


def bool_to_int(array):
    array_r = np.where(array == True, 100, 0)
    return  array_r

def int_to_bool(array):
    array_r = np.where(array > 50, True, False)
    return array_r

def generate_qrcode(data, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=5, border=4):
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

    array = bool_to_int(np.array(img))
    return array

def decode_qrcode(data):
    qrImg = Image.fromarray(np.uint8(data))
    codes = zbarlight.scan_codes('qrcode', qrImg)
    for i in codes:
        codes = i.decode('utf-8', 'ignore')

    return codes

def qrsizeChange(array):
    m_f = np.log2(len(array))
    m_i = np.ceil(m_f)
    next_pow2 =  int(np.log2(2 ** m_i))
    img = Image.fromarray(np.uint8(array))
    img = img.resize((int(math.pow(2, next_pow2)), int(math.pow(2, next_pow2))))
    img = np.asarray(img)
    img.flags.writeable = True
    return img


def main():
    # encode
    tmp = generate_qrcode('私はオーストラリアでInternshipをしています！')
    # decode
    tmp_a = qrsizeChange(tmp)
    print(decode_qrcode(tmp_a))



if __name__ == '__main__':
    main()
import qrcode
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


def main():
    tmp = generate_qrcode('あ，4％＄＠?>/kfgejabjdfk確かに')
    # decode部分を追加
    print(decode_qrcode(tmp))



if __name__ == '__main__':
    main()
import pywt
import numpy as np
from PIL import Image


def img_normalization(src_img):
    norm_img = (src_img - np.min(src_img)) / (np.max(src_img) - np.min(src_img))
    return norm_img


def merge_img(cA, cH_V_D):
    cH, cV, cD = cH_V_D
    # cH = img_normalization(cH)  # 外してもok
    # cV = img_normalization(cV)  # 外してもok
    # cD = img_normalization(cD)  # 外してもok
    # cA = cA[0:cH.shape[0], 0:cV.shape[1]]  # 元画像が2の累乗ピクセルでない場合の端数調整。小さい方に
    return np.vstack((np.hstack((cA, cH)), np.hstack((cV, cD))))  # [cA, cH]を[cV, cD]縦にくっつける[低周波，y方向高周波],[x方向高周波，xy方向高周波]


def coeffs_show(coeffs):
    coeffs0 = coeffs[0]
    # coeffs0 = img_normalization(coeffs0) # 外してもok
    merge = coeffs0
    for i in range(1, len(coeffs)):
        merge = merge_img(merge, coeffs[i])  # ４つの画像を合わせていく
    Image.fromarray(np.uint8(merge)).show()


def list_to_textfile(lst, name):
    f = open(name, 'w')
    for i in lst:
        f.write(str(i)+'\n')
    f.close()


def main():
    imgname = 'blena512.bmp'
    wavelet = 'db1' # wavelist.txtにどれを指定できるか書いてある
    level = 1

    img = np.array(Image.open('../images/'+imgname), 'f')
    gray_img = Image.fromarray(np.uint8(img)).convert('L')

    # Wavelet変換
    coeffs = pywt.wavedec2(gray_img,wavelet=wavelet,level=level)
    coeffs_show(coeffs)

    # 複数回ウェーブレットを行いたい場合（検討中）
    # coeffs = pywt.dwt2(gray_img, wavelet=wavelet)
    # cA, (cH,cV,cD) = coeffs
    # 電子透かしで高周波成分を操作する場合cH_V_Dのどれかを選択する
    # coeffs_show(coeffs)
    # coeffs = pywt.dwt2(cA, wavelet=wavelet)
    # coeffs_show(coeffs)


    # 復調
    # tmp = pywt.waverec2(coeffs, wavelet=wavelet)
    # Image.fromarray(np.uint8(tmp)).show()



if __name__ == '__main__':
    main()





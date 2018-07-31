import pywt
import math
import qrcode
import numpy as np
from PIL import Image

outImagepath = '../images/result/'
imgname = 'balls.JPG'
wavelet = 'db1'  # wavelist.txtにどれを指定できるか書いてある
level = 1

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

def psnr(cover, stego):
	mse = np.mean((cover-stego)**2)
	if mse == 0:
		return 100
	PIXEL_MAX = 255.0

	return 20 * math.log10(PIXEL_MAX/math.sqrt(mse))


def get_ycbcr_array(name: str):
	pil_img = Image.open('../images/'+name)
	pil_y, pil_cr, pil_cb = pil_img.convert('YCbCr').split()
	y = np.asarray(pil_y)
	cr = np.asarray(pil_cr)
	cb = np.asarray(pil_cb)
	y.flags.writeable = True
	cr.flags.writeable = True
	cb.flags.writeable = True
	return [y, cr, cb]


def save_ycbcr_as_img(name: str, y, cr, cb):
	pil_y = Image.fromarray(np.uint8(y))
	pil_cr = Image.fromarray(np.uint8(cr))
	pil_cb = Image.fromarray(np.uint8(cb))
	pil_img = Image.merge('YCbCr', (pil_y, pil_cr, pil_cb)).convert('RGB')
	pil_img.save('../images/result/' + name)



def main1():
	# 画像を取得しグレースケールに変換
	# DWTを行いxy高周波成分を全て0に置換する
	# 画像に戻す


	img = np.array(Image.open('../images/' + imgname), 'f')
	gray_img = Image.fromarray(np.uint8(img)).convert('L')
	gray_img.save(outImagepath + 'ball_gray.JPG')

	# Wavelet変換
	# coeffs = pywt.wavedec2(gray_img,wavelet=wavelet,level=level) #wavedec2 [cAn, (cHn, cVn, cDn), … (cH1, cV1, cD1)] : list  are return.
	# coeffs_show(coeffs)

	# 別Ver（1度のウェーブレットのビット置換）
	coeffs = pywt.dwt2(gray_img, wavelet=wavelet)
	cA, (cH, cV, cD) = coeffs
	# 電子透かしで高周波成分を操作する場合cH_V_Dのどれかを選択する(半分のピクセル数になる)とりあえずcDを全部0にしてみる
	cD_a = np.full_like(cD, 0.000)
	coeffs_a = cA, (cH, cV, cD_a)

	coeffs_show(coeffs)
	coeffs_show(coeffs_a)

	# 復調
	tmp = pywt.waverec2(coeffs_a, wavelet=wavelet)
	Image.fromarray(np.uint8(tmp)).save(outImagepath + 'ball_embed.JPG')


def main2():
	# 画像を取得し輝度値に対してDWTを行う
	# xyの高周波成分を任意のデータで置換して画像を表示する
	img = np.array(Image.open('../images/' + imgname), 'f')
	img_y, img_cr, img_cb = get_ycbcr_array(imgname)
	size = len(img)

	# 別Ver（1度のウェーブレットのビット置換）
	coeffs = pywt.dwt2(img_y, wavelet=wavelet)
	cA, (cH, cV, cD) = coeffs
	# 電子透かしで高周波成分を操作する場合cH_V_Dのどれかを選択する(半分のピクセル数になる)とりあえずcDを全部0にしてみる
	cD_a = np.full_like(cD, 0.000)
	coeffs_replace = cA, (cH, cV, cD_a)

	coeffs_show(coeffs)
	coeffs_show(coeffs_replace)

	# 復調
	img_y_f = pywt.waverec2(coeffs_replace, wavelet=wavelet)
	save_ycbcr_as_img('dwt_result.JPG', img_y_f, img_cr, img_cb)



if __name__ == '__main__':
	main2()





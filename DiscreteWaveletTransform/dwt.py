import pywt
import math
import qrcode
import numpy as np
from PIL import Image


outImgPath = '../images/result/'
imgPath    = '../images/'
imgName    = 'balls.JPG'
wavelet    = 'db1'  # wavelist.txtにどれを指定できるか書いてある
level      = 1


def imgNormalization(src_img):
	norm_img = (src_img - np.min(src_img)) / (np.max(src_img) - np.min(src_img))
	return norm_img


def mergeImg(cA, cH_V_D):
	cH, cV, cD = cH_V_D
	# cH = imgNormalization(cH)  # 外してもok
	# cV = imgNormalization(cV)  # 外してもok
	# cD = imgNormalization(cD)  # 外してもok
	cA = cA[0:cH.shape[0], 0:cV.shape[1]]  # 元画像が2の累乗ピクセルでない場合の端数調整。小さい方に
	return np.vstack((np.hstack((cA, cH)), np.hstack((cV, cD))))  # [cA, cH]を[cV, cD]縦にくっつける[低周波，y方向高周波],[x方向高周波，xy方向高周波]


def coeffsShow(coeffs):
	coeffs0 = coeffs[0]
	# coeffs0 = imgNormalization(coeffs0) # 外してもok
	merge = coeffs0
	for i in range(1, len(coeffs)):
		merge = mergeImg(merge, coeffs[i])  # ４つの画像を合わせていく
	Image.fromarray(np.uint8(merge)).show()


def listToTextfile(lst, name):
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


def getYcbcrArray(name):
	pil_img = Image.open(imgPath+name)
	pil_y, pil_cr, pil_cb = pil_img.convert('YCbCr').split()
	y = np.asarray(pil_y)
	cr = np.asarray(pil_cr)
	cb = np.asarray(pil_cb)
	y.flags.writeable = True
	cr.flags.writeable = True
	cb.flags.writeable = True
	return [y, cr, cb]


def saveYcbcrAsImg(name: str, y, cr, cb):
	pil_y = Image.fromarray(np.uint8(y))
	pil_cr = Image.fromarray(np.uint8(cr))
	pil_cb = Image.fromarray(np.uint8(cb))
	pil_img = Image.merge('YCbCr', (pil_y, pil_cr, pil_cb)).convert('RGB')
	pil_img.save(outImgPath+name)


def getImgSizeAndData(imgname):
	img = np.array(Image.open(imgPath+imgname), 'f')
	img_y, img_cr, img_cb = getYcbcrArray(imgname)
	width = img.shape[1]
	height = img.shape[0]
	return width, height, img_y, img_cr, img_cb


def main_tmp():
	# これいる？
	# 画像を取得しグレースケールに変換
	# DWTを行いxy高周波成分を全て0に置換する
	# 画像に戻す

	img = np.array(Image.open(imgPath+imgName), 'f')
	gray_img = Image.fromarray(np.uint8(img)).convert('L')
	gray_img.save(outImgPath+imgName)

	# Wavelet変換
	# coeffs = pywt.wavedec2(gray_img,wavelet=wavelet,level=level) #wavedec2 [cAn, (cHn, cVn, cDn), … (cH1, cV1, cD1)] : list  are return.
	# coeffs_show(coeffs)

	# 別Ver（1度のウェーブレットのビット置換）
	coeffs = pywt.dwt2(gray_img, wavelet=wavelet)
	cA, (cH, cV, cD) = coeffs
	# 電子透かしで高周波成分を操作する場合cH_V_Dのどれかを選択する(半分のピクセル数になる)とりあえずcDを全部0にしてみる
	cD_a = np.full_like(cD, 0.000)
	coeffs_a = cA, (cH, cV, cD_a)

	coeffsShow(coeffs)
	coeffsShow(coeffs_a)

	# 復調
	tmp = pywt.waverec2(coeffs_a, wavelet=wavelet)
	Image.fromarray(np.uint8(tmp)).save(outImgPath+'dwt_'+imgName)


def main():
	# 画像を取得し輝度値に対してDWTを行う
	# xyの高周波成分を任意のデータで置換して画像を表示する
	width, hight, img_y, img_cr, img_cb = getImgSizeAndData(imgName)

	# レベル1のウェーブレット -> ビット置換
	coeffs = pywt.dwt2(img_y, wavelet=wavelet)
	cA, (cH, cV, cD) = coeffs
	# 電子透かしで高周波成分を操作する場合cH_V_Dのどれかを選択する(半分のピクセル数になる)とりあえずcDを全部0にしてみる
	cD_a = np.full_like(cD, 10.000)
	coeffs_r = cA, (cH, cV, cD_a)

	coeffsShow(coeffs)
	coeffsShow(coeffs_r)

	# 復調
	img_y_f = pywt.waverec2(coeffs_r, wavelet=wavelet)
	# 輝度値がマイナスの場合にマイナスを消す処理(+255)を追加するけど，抽出がうまく行かなくなる可能性あり(画像も綺麗にならんかった)
	img_y_f = np.where(img_y_f < 0.0, 255+img_y_f, img_y_f)

	saveYcbcrAsImg('dwt_result'+imgName, img_y_f, img_cr, img_cb)



if __name__ == '__main__':
	main()





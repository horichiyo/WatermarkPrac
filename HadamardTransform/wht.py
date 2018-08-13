import math
import sys
import numpy as np
from PIL import Image

outImgPath = '../images/result/'
imgPath    = '../images/'
imgName    = 'lena512.bmp'


def generateHadamard(N):
	hadmard = np.asarray([[1.0,1.0],[1.0,-1.0]])
	if (N != 1):
		hadamard_copy = hadmard.copy()
		for i in range (1, N):
			hadmard =  np.hstack((hadmard, hadmard))
			hadamard_copy =  np.hstack((hadamard_copy, -hadamard_copy))
			hadmard = np.vstack((hadmard, hadamard_copy))
			hadamard_copy = hadmard.copy()
	return hadmard


def sequence(hadamardArray):
	length = len(hadamardArray)
	index =  np.array([0]*length)

	# 並び替えるためのインデックスを計算する
	for i in range(length):
		tmp=0
		for j in range(length-1):
			tmp += abs(hadamardArray[i,j] - hadamardArray[i,j+1])
		tmp /= 2
		index[i] = int(tmp)

	index = np.argsort(index)

	# for-loopを使って並び替える
	return hadamardArray[index]


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


def sizeCheck(width: int, height: int):
	# 2のべき乗かどうか判断して2のべき乗かつ画像の縦横が等しくなければ終了 等しければ2のN乗になってるかを返す
	if width != height :
		print('The image must be square.')
		sys.exit(1)

	# (n & (n - 1)) == 0　なら2のべき乗 -> ビット演算で高速化可能
	while (((width % 2) == 0) and width > 1):
		width /= 2

	if width != 1:
		print('Size must be a power of 2.')
		sys.exit(1)

	return int(math.log(height, 2))


def hadamardTransform(hadamard, data, N):
	_G_tmp = np.dot(hadamard, data)
	return np.dot(_G_tmp, hadamard) / 2**N


def inverseHadamardTransform(hadamard, G, N):
	_F_tmp = np.dot(hadamard, G)
	return np.dot(_F_tmp, hadamard) / 2**N




def main():
	img_y, img_cr, img_cb = getYcbcrArray(imgName)
	size = len(img_y)

	y, _,_ = getYcbcrArray('lake.bmp')


	# 2のべき乗かつ画像が正方形であるかどうかのチェック
	N = sizeCheck(size, len(img_y[0]))

	# 並べ替え済みアダマール行列の生成
	hadamard = sequence(generateHadamard(N))

	# アダマール変換 G -> 変換係数
	G = hadamardTransform(hadamard, img_y, N)
	for i in range(len(y)):
		for j in range(len(y)):
			G[len(y)+i,len(y)+j] = y[i,j]



	# 復調 変換係数G -> F
	F = inverseHadamardTransform(hadamard, G, N)

	Image.fromarray(np.uint8(F)).show()

	ex_g = hadamardTransform(hadamard, F, N)
	ex = ex_g[256:, 256:]
	Image.fromarray(np.uint8(ex)).show()

	# saveYcbcrAsImg('wht_'+imgName, img_y, img_cr, img_cb)


if __name__ == '__main__':
	main()



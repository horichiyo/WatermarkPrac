import math
import sys
import numpy as np
from PIL import Image


def generate_hadamard(N):
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


def size_check(length: int, height: int):
	# 2のべき乗かどうか判断して2のべき乗かつ画像の縦横が等しくなければ終了 等しければ2のN乗になってるかを返す
	if length != height :
		print('The image must be square.')
		sys.exit(1)

	# (n & (n - 1)) == 0　なら2のべき乗 -> ビット演算で高速化可能
	while (((length % 2) == 0) and length > 1):
		length /= 2

	if length != 1:
		print('Size must be a power of 2.')
		sys.exit(1)

	return int(math.log(height, 2))


def main():
	imgname = 'lena512.bmp'
	img = np.array(Image.open('../images/' + imgname), 'f')
	img_y, img_cr, img_cb = get_ycbcr_array(imgname)
	size = len(img)

	# 2のべき乗かつ画像が正方形であるかどうかのチェック
	N = size_check(size, len(img[0]))

	hadamard = sequence(generate_hadamard(N))

	# アダマール変換 G -> 変換係数
	G_tmp = np.dot(hadamard, img_y)
	G = np.dot(G_tmp, hadamard) / 2**N

	# 復調
	F_tmp = np.dot(hadamard, G)
	F = np.dot(F_tmp, hadamard) / 2**N


	Image.fromarray(np.uint8(F)).show()
	save_ycbcr_as_img(imgname, img_y, img_cr, img_cb)


if __name__ == '__main__':
	main()
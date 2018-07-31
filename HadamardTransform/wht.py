import math
import numpy as np
from PIL import Image


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


def get_ycbcr_array(name: str):
    pil_img = Image.open('../images/'+name)
    pil_y, pil_cr, pil_cb = pil_img.convert("YCbCr").split()
    y = np.asarray(pil_y)
    cr = np.asarray(pil_cr)
    cb = np.asarray(pil_cb)
    y.flags.writeable = True
    cr.flags.writeable = True
    cb.flags.writeable = True
    return [y, cr, cb]
    # return np.array([y,cr,cb])


def main():
	imgname = 'lena256.bmp'
	img = np.array(Image.open('../images/' + imgname), 'f')
	gray_img = Image.fromarray(np.uint8(img)).convert('L')
	gray_img_f = np.array(gray_img, 'f')
	img_y, cb, cr = get_ycbcr_array(imgname)

	# N -> 2**N
	N = int(math.log(len(gray_img_f), 2))
	hadamard = sequence(generateHadamard(N))

	# G = (hadamard*img_y*hadamard)/math.sqrt(2**N)
	a = np.dot(hadamard, img_y)
	G = np.dot(a, hadamard)/ 2**N

	# rev = (hadamard*G*hadamard)*math.sqrt(2**N)
	b = np.dot(hadamard, G)
	rev = np.dot(b, hadamard)/ 2**N

	print(G)

	print(rev)


	Image.fromarray(np.uint8(rev)).show()





if __name__ == '__main__':
	main()
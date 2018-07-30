import numpy as np
from PIL import Image

def generateHadamard(N):
	hadmard = np.asarray([[1,1],[1,-1]])
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


def main():
	# N -> 2**N
	N = 4
	# hadamard = generateHadamard(N)
	# print(sequence(generateHadamard(N)))


	# 画像を読み込み，グレースケールに変換する
	# 画像の大きさに合わせたアダマール行列を生成する
	# アダマール行列とグレースケールに変換した画像の輝度値に対してアダマール変換を行う
	# 変換後の画像を表示する
	# アダマール行列と変換後の画像を用いて逆変換を行う




if __name__ == '__main__':
	main()
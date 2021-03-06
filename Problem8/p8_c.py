import sys
import numpy as np

def dec2bin(num):
    l = []
    if num < 0:
        return '-' + dec2bin(abs(num))
    while True:
        num, remainder = divmod(num, 2)
        l.append(str(remainder))
        if num == 0:
        	bin12 = ''.join(l[::-1]).zfill(12)
        	return bin12[::-1]

file = 'dataset.dat'
samples = np.loadtxt(file, dtype = int)

# 0
count_1 = np.zeros((1, 2))
# joint of 10, 20, 30, 40
count_2 = np.zeros((4, 2))
# joint of 1234
count_3 = np.zeros((1, 16))
# joint 1234_5 - 1234_11
count_4 = np.zeros((7, 16))

prob_1 = 0
prob_2 = np.zeros((4, 2))
prob_3 = np.zeros((7, 16))

index_list = ['1111', '1110', '1101', '1100', '1011', '1010', '1001', '1000', '0111', '0110', '0101', '0100', '0011', '0010', '0001', '0000']

for sample in samples:
	sample = dec2bin(sample)
	if sample[0] == '1':
		count_1[0, 0] += 1
		for i in range(1, 5):
			if sample[i] == '1':
				count_2[i-1, 0] += 1
	if sample[0] == '0':
		count_1[0, 1] += 1
		for j in range(1, 5):
			if sample[j] == '1':
				count_2[j-1, 1] += 1	

	for index in range(len(index_list)):
		if sample[1:5] == index_list[index]:
			count_3[0, index] += 1
			for k in range(5, 12):
				if sample[k] == '1':
					count_4[k-5, index] += 1	

prob_1 = count_1[0, 0] / count_1.sum()

prob_2[:, 0] = count_2[:, 0] / count_1[0, 0]
prob_2[:, 1] = count_2[:, 1] / count_1[0, 1]

for l in range(0, 16):
	prob_3[:, l] = count_4[:, l] / count_3[0, l]

print(prob_1)
print(prob_2)
print(prob_3)






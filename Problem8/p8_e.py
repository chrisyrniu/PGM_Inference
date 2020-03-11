import sys
import numpy as np
from Factor import Factor

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

def prob_estimate(file):

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

	return prob_1, prob_2, prob_3

def generate_phi_values(sequence):
	probs1 = sequence[::-1]
	probs2 = 1 - probs1
	probs = np.hstack((probs1, probs2))

	return probs

def generate_factors(prob_1, prob_2, prob_3):
	phi0 = Factor(['0'], [2], [1-prob_1, prob_1])
	phi1 = Factor(['1', '0'], [2,2], generate_phi_values(prob_2[0, :]))
	phi2 = Factor(['2', '0'], [2,2], generate_phi_values(prob_2[1, :]))
	phi3 = Factor(['3', '0'], [2,2], generate_phi_values(prob_2[2, :]))
	phi4 = Factor(['4', '0'], [2,2], generate_phi_values(prob_2[3, :]))
	phi5 = Factor(['5', '1', '2', '3', '4'], [2,2,2,2,2], generate_phi_values(prob_3[0, :]))
	phi6 = Factor(['6', '1', '2', '3', '4'], [2,2,2,2,2], generate_phi_values(prob_3[1, :]))
	phi7 = Factor(['7', '1', '2', '3', '4'], [2,2,2,2,2], generate_phi_values(prob_3[2, :]))
	phi8 = Factor(['8', '1', '2', '3', '4'], [2,2,2,2,2], generate_phi_values(prob_3[3, :]))
	phi9 = Factor(['9', '1', '2', '3', '4'], [2,2,2,2,2], generate_phi_values(prob_3[4, :]))
	phi10 = Factor(['10', '1', '2', '3', '4'], [2,2,2,2,2], generate_phi_values(prob_3[5, :]))
	phi11 = Factor(['11', '1', '2', '3', '4'], [2,2,2,2,2], generate_phi_values(prob_3[6, :]))

	return [phi0, phi1, phi2, phi3, phi4, phi5, phi6, phi7, phi8, phi9, phi10, phi11]

def set_product(factors):
	if len(factors) == 1:
		return factors[0]
	else:
		fac = factors[0]
		for i in range(len(factors)-1):
			fac = factors[i+1].product(fac, inplace=False)

	return fac

def variable_elimination(factor_list, evidence, order):
	factors = factor_list
	for var in order:
		isEvidence = False
		sumprod_list = []
		for factor in factors:
			if var in factor.variables:
				sumprod_list.append(factor)

		factors = list(set(factors) - set(sumprod_list))

		for evid in evidence:
			if var == evid[0]:
				isEvidence = True
				for pot in sumprod_list:
					pot.reduce([evid])
					factors.append(pot)

		if not isEvidence:
			message = set_product(sumprod_list)
			message.marginalize([var])
			factors.append(message)

	if len(factors) > 1:
		return set_product(factors)
	else:
		return factors[0]

if __name__ == "__main__":

	prob_1, prob_2, prob_3 = prob_estimate('dataset.dat')

	factors = generate_factors(prob_1, prob_2, prob_3)
	evidence1 = [('8', 1), ('11', 1)]
	order1 = ['8','11','5','6','7','9','10','2','3','4','0']
	distribution1 = variable_elimination(factors, evidence1, order1)
	distribution1.normalize()
	p1 = distribution1.values[1]
	print(p1)

	factors = generate_factors(prob_1, prob_2, prob_3)
	evidence2 = [('4', 1)]
	order2 = ['4', '5', '6', '0', '1', '2', '3']
	distribution2 = variable_elimination(factors, evidence2, order2)
	distribution2.normalize()
	p2 = distribution2.values
	print(p2)
	print(distribution2.variables)

	factors = generate_factors(prob_1, prob_2, prob_3)
	evidence3 = [('0', 1)]
	order3 = ['0', '5', '6', '7', '8', '9', '11', '1', '2', '3', '4']
	distribution3 = variable_elimination(factors, evidence3, order3)
	distribution3.normalize()
	p3 = distribution3.values[1]
	print(p3)






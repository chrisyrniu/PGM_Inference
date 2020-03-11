import numpy as np 
from Factor import Factor

a = [x for x in range(1, 101)]
b = np.array(a).reshape(10, 10).transpose()

for k in range(10):
	# initialize potentials
	for i in range(9):
		if i == 0:
			col_pot = Factor([np.str(b[i,k]), np.str(b[i+1,k])], [2, 2], [1, 0, 0, 1])
		else:
			pot = Factor([np.str(b[i,k]), np.str(b[i+1,k])], [2, 2], [1, 0, 0, 1])
			col_pot.product(pot, log=True)
	if k != 9:		
		for j in range(10):
			if j == 0:
				interact_pot = Factor([np.str(b[j,k]), np.str(b[j,k+1])], [2, 2], [1, 0, 0, 1])
			else:
				pot = Factor([np.str(b[j,k]), np.str(b[j,k+1])], [2, 2], [1, 0, 0, 1])
				interact_pot.product(pot, log=True)

	# message passing 
	if k == 0:
		message = col_pot.product(interact_pot, inplace=False, log=True)
		message.marginalize(col_pot.variables, log=True)	

	elif 0 < k < 9:
		message = col_pot.product(message, inplace=False, log=True)
		message.product(interact_pot, log=True)
		message.marginalize(col_pot.variables, log=True)
	else:
		message = col_pot.product(message, inplace=False, log=True)
		message.marginalize(col_pot.variables, log=True)

print(message.values)


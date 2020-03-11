import numpy as np 

class Factor(object):

	def __init__(self, variables, cardinality, values):

		values = np.array(values, dtype=float)

		self.variables = list(variables)
		self.cardinality = np.array(cardinality, dtype=int)
		self.values = values.reshape(self.cardinality)


	def copy(self):

		return Factor(self.variables, self.cardinality, self.values)

	def get_cardinality(self, variables):

		return {var: self.cardinality[self.variables.index(var)] for var in variables}


	def product(self, phi_other, inplace=True, log=False):

		if inplace:
			phi = self
		else:
			phi = self.copy()

		if isinstance(phi_other, (int, float)):
			phi.values *= phi_other
		else:
			phi_other = phi_other.copy()

		extra_vars = set(phi_other.variables) - set(phi.variables)

		if extra_vars:
			slice_ = [slice(None)] * len(phi.variables)
			slice_.extend([np.newaxis] * len(extra_vars))
			phi.values = phi.values[tuple(slice_)]
			phi.variables.extend(extra_vars)
			new_var_card = phi_other.get_cardinality(extra_vars)
			phi.cardinality = np.append(phi.cardinality, [new_var_card[var] for var in extra_vars])

		extra_vars = set(phi.variables) - set(phi_other.variables)

		if extra_vars:
			slice_ = [slice(None)] * len(phi_other.variables)
			slice_.extend([np.newaxis] * len(extra_vars))
			phi_other.values = phi_other.values[tuple(slice_)]

			phi_other.variables.extend(extra_vars)
		
		for axis in range(phi.values.ndim):
			exchange_index = phi_other.variables.index(phi.variables[axis])
			phi_other.variables[axis], phi_other.variables[exchange_index] = (
                phi_other.variables[exchange_index],
                phi_other.variables[axis],
            )
			phi_other.values = phi_other.values.swapaxes(axis, exchange_index)

		if not log:
			phi.values = phi.values * phi_other.values
		else:
			phi.values = phi.values + phi_other.values

		if not inplace:
			return phi

	def marginalize(self, variables, inplace=True, log=False):

		if inplace:
			phi = self
		else:
			phi = self.copy()   

		var_indexes = [phi.variables.index(variable) for variable in variables]

		index_to_keep = sorted(set(range(len(self.variables))) - set(var_indexes))	
		phi.variables = [phi.variables[index] for index in index_to_keep]
		phi.cardinality = phi.cardinality[index_to_keep]

		if not log:
			phi.values = np.sum(phi.values, axis=tuple(var_indexes))
		# logsumexp trick
		else:
			# phi.values = np.log(np.sum(np.exp(phi.values), axis=tuple(var_indexes)))
			shift = np.max(phi.values, axis=tuple(var_indexes))
			phi.values = shift + np.log(np.sum(np.exp(phi.values - shift), axis=tuple(var_indexes)))
		if not inplace:
			return phi




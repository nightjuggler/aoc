import re
import sys

class Fraction(object):
	def __init__(self, num=0, denom=1):
		assert isinstance(num, int) and isinstance(denom, int)
		if not denom:
			self.num = 1
			self.denom = 0
			return
		if denom < 0:
			num = -num
			denom = -denom
		gcd, x = num, denom
		while x:
			gcd, x = x, gcd % x
		self.num = num // gcd
		self.denom = denom // gcd

	def is_integer(self): return self.denom == 1
	def is_positive(self): return self.num > 0 and self.denom
	def is_negative(self): return self.num < 0 and self.denom
	def frac(self):
		return Fraction(self.num % self.denom, self.denom)

	def __hash__(self):
		return hash((self.num, self.denom))
	def __bool__(self):
		return self.num != 0
	def __repr__(self):
		return str(self.num) if self.denom == 1 else f'{self.num}/{self.denom}'
	def __format__(self, spec):
		return format(str(self), spec)

	def __add__(self, other):
		return Fraction(self.num*other.denom + other.num*self.denom, self.denom*other.denom)
	def __sub__(self, other):
		return Fraction(self.num*other.denom - other.num*self.denom, self.denom*other.denom)
	def __mul__(self, other):
		return Fraction(self.num*other.num, self.denom*other.denom)
	def __truediv__(self, other):
		return Fraction(self.num*other.denom, self.denom*other.num) if other.denom else Fraction(1, 0)
	def __neg__(self):
		return Fraction(-self.num, self.denom)
	def __abs__(self):
		return Fraction(abs(self.num), self.denom)
	def __invert__(self):
		return Fraction(self.denom, self.num)
	def __round__(self, ndigits=None):
		return round(self.num / self.denom, ndigits)

	def __lt__(self, other): return self.num*other.denom < other.num*self.denom
	def __le__(self, other): return self.num*other.denom <= other.num*self.denom
	def __eq__(self, other): return self.denom == other.denom and self.num == other.num
	def __ne__(self, other): return self.denom != other.denom or self.num != other.num
	def __gt__(self, other): return self.num*other.denom > other.num*self.denom
	def __ge__(self, other): return self.num*other.denom >= other.num*self.denom

def dual_simplex_pivot(matrix, cz):
	rhs = [row[-1] for row in matrix]
	min_rhs = min(rhs)
	if not min_rhs.is_negative(): return None
	pivot_row = rhs.index(min_rhs)
	pivot_col = None
	min_entry = None
	for i, e in enumerate(matrix[pivot_row][:-1]):
		if e.is_negative():
			e = abs(cz[i] / e)
			if pivot_col is None or e < min_entry:
				min_entry = e
				pivot_col = i
	if pivot_col is None:
		sys.exit(f'No pivot in row {pivot_row}!')
	return pivot_row, pivot_col

def simplex_pivot(matrix, cz):
	max_cz = max(cz)
	if not max_cz.is_positive(): return None
	pivot_col = cz.index(max_cz)
	pivot_row = None
	min_entry = None
	for i, row in enumerate(matrix):
		e = row[pivot_col]
		if e.is_positive():
			e = row[-1] / e
			if pivot_row is None or e < min_entry:
				min_entry = e
				pivot_row = i
	if pivot_row is None:
		sys.exit(f'No pivot in column {pivot_col}!')
	return pivot_row, pivot_col

def get_frac_row(matrix):
	for row in matrix:
		if not row[-1].is_integer() and not all(col.is_integer() for col in row[:-1]):
			return row
	return None

def solve(matrix, rhs):
	#
	# Use the simplex algorithm, Big M method, and cutting-plane method:
	# Because we have equalities and not inequalities, instead of adding a slack variable
	# with objective value 0 for each row, add an artificial variable with objective value
	# -big_m for each row to establish a basis. The columns associated with these artificial
	# variables are removed as they leave the basis.
	# Because we want to minimize instead of maximize the sum of the variables corresponding
	# to the columns of the initial matrix, the objective is initialized to -1 for each column
	# of the intial matrix (and -big_m for each column associated with an artificial variable).
	# After an optimal (but likely non-integer) solution is found, the cutting-plane method
	# is used to add one constraint at a time until an all-integer solution is found.
	#
	num_rows = len(matrix)
	assert len(rhs) == num_rows > 0
	num_cols = len(matrix[0])
	assert num_cols and all(len(row) == num_cols for row in matrix)

	for i, (row, rhs) in enumerate(zip(matrix, rhs)):
		ext = [0] * num_rows
		ext[i] = 1
		row.extend(ext)
		row.append(rhs)

	one = Fraction(1)
	zero = Fraction(0)
	big_m = Fraction(2**30)
	objective = [Fraction(-1)] * num_cols + [-big_m] * num_rows
	bigm_size = num_cols + num_rows
	matrix = [list(map(Fraction, row)) for row in matrix]
	basis = list(range(num_cols, num_cols + num_rows))

	while True:
		cb = [objective[b] for b in basis]
		z = [sum((aj*cj for aj, cj in zip(col, cb)), start=zero) for col in zip(*matrix)]
		cz = [cj - zj for cj, zj in zip(objective, z)]

		pivot = dual_simplex_pivot(matrix, cz) or simplex_pivot(matrix, cz)
		if not pivot:
			if not (row := get_frac_row(matrix)): break
			new_row = [-e.frac() for e in row]
			new_row.insert(-1, one)
			for row in matrix: row.insert(-1, zero)
			matrix.append(new_row)
			objective.append(zero)
			basis.append(len(objective)-1)
			pivot = dual_simplex_pivot(matrix, cz)

		pivot_row, pivot_col = pivot
		if num_cols <= (basis_col := basis[pivot_row]) < bigm_size:
			# An artificial variable is leaving the basis. Remove its column.
			bigm_size -= 1
			if pivot_col > basis_col: pivot_col -= 1
			for row in matrix: del row[basis_col]
			del objective[basis_col]
			for i, b in enumerate(basis):
				if b > basis_col: basis[i] -= 1

		basis[pivot_row] = pivot_col
		pivot_row = matrix[pivot_row]
		if (pivot := pivot_row[pivot_col]) != one:
			pivot = ~pivot
			pivot_row[:] = [pivot*pj for pj in pivot_row]
		for row in matrix:
			if row is not pivot_row and (m := row[pivot_col]):
				row[:] = [rj - m*pj for rj, pj in zip(row, pivot_row)]

	x = [matrix[basis.index(i)][-1] if i in basis else zero for i in range(num_cols)]
	return -z[-1], x

def check_result(buttons, joltages, presses):
	jolts = [Fraction(0)] * len(joltages)
	for button, press in zip(buttons, presses):
		for j in button: jolts[j] += press
	return jolts == list(map(Fraction, joltages))

def main():
	result = zero = Fraction(0)
	pattern = re.compile(r'^\[[#.]+\](?: \(\d(?:,\d)*\))+ \{\d+(?:,\d+)*\}$')
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f'Line {line_num} doesn\'t match the expected pattern!')
		lights, *buttons, joltages = line.split()
		buttons = [set(int(i) for i in button[1:-1].split(',')) for button in buttons]
		joltages = [int(i) for i in joltages[1:-1].split(',')]

		matrix = [[int(j in b) for b in buttons] for j in range(len(joltages))]
		z, x = solve(matrix, joltages)
		x_sum = sum(x, start=zero)
		assert z == x_sum
		assert check_result(buttons, joltages, x)
		result += x_sum
	print(result)
main()

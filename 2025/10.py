import operator
import re
import sys
from scipy.optimize import linprog

def solve1(machine):
	buttons, lights = machine
	if not lights: return 0
	buttons = [sum(1<<i for i in button) for button in buttons]
	states = {0}
	seen = {0}
	presses = 0
	while states:
		presses += 1
		new_states = set()
		for state in states:
			for button in buttons:
				new_state = state ^ button
				if new_state == lights: return presses
				if new_state not in seen:
					seen.add(new_state)
					new_states.add(new_state)
		states = new_states
	return None

def check_result(buttons, joltages, presses):
	jolts = [0]*len(joltages)
	for button, press in zip(buttons, presses):
		for j in button: jolts[j] += press
	return jolts == joltages

def solve2_scipy(machine, full_result=False):
	buttons, joltages = machine
	matrix = [[int(j in b) for b in buttons] for j in range(len(joltages))]

	# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html

	result = linprog(c=[1]*len(buttons), A_eq=matrix, b_eq=joltages, integrality=1)
	return result if full_result else round(sum(result.x)) if result.success else None

def rowstr(row):
	return f'[{','.join(f'{x:3}' for x in row[:-1])}] = {row[-1]}'

def print_result(x):
	print(f'[{','.join(f'{n:3}' for n in x)}] => {sum(x)}')

def reduce_matrix(matrix): # Gaussian elimination (aka row reduction)
	num_rows = len(matrix)
	num_cols = len(matrix[0])-1 # The last column is the joltage requirement
	matrix.sort(reverse=True)

	for y in range(min(num_rows, num_cols)):
		while True:
			row1 = matrix[y]
			lead = row1[y]
			if lead == 0 or lead == 1: break
			for row2 in matrix[y+1:]:
				if row2[y] == 1:
					row1[:], row2[:] = row2[:], row1[:]
					break
				if lead - row2[y] == 1:
					row1[:] = [a - b for a, b in zip(row1, row2)]
					break
			else:
				for row2 in matrix[y+1:]:
					if lead >= row2[y] > 0:
						row1[:] = [a - b for a, b in zip(row1, row2)]
						break
				else:
					# Cannot make leading entry 1
					break
				matrix[y:] = sorted(matrix[y:], reverse=True)
		if lead == 0: continue
		if lead != 1: break

		for row2 in matrix[y+1:]:
			lead = row2[y]
			if lead == 0: continue
			row2[:] = [a - b*lead for a, b in zip(row2, row1)]
			for lead in row2:
				if lead: break
			if lead < 0:
				row2[:] = [-a for a in row2]

		matrix[y+1:] = sorted(matrix[y+1:], reverse=True)

	while matrix:
		if any(matrix[-1]): break
		matrix.pop()

def gen_values(max_values, sum_values=0):
	values = (0,)*len(max_values)
	yield (sum_values, values)
	previous_set = {values}
	while previous_set:
		sum_values += 1
		current_set = set()
		for i, max_value in enumerate(max_values):
			for previous in previous_set:
				if previous[i] == max_value: continue
				values = list(previous)
				values[i] += 1
				values = tuple(values)
				if values not in current_set:
					yield (sum_values, values)
					current_set.add(values)
		previous_set = current_set

def make_table(matrix, max_presses):
	table = []
	num_cols = len(max_presses)
	fixed = [False]*num_cols
	indices = []

	for row in matrix[::-1]:
		rhs = row[-1]
		fixed_entries = [row[i] for i in indices]
		entries = []
		max_values = []
		for i in range(num_cols):
			if not fixed[i] and row[i]:
				indices.append(i)
				entries.append(row[i])
				max_values.append(max_presses[i])
				fixed[i] = True
		lead = entries[0] if entries else 0
		can_break = lead > 0 and all(a == lead for a in entries)
		table.append((can_break, entries, max_values, fixed_entries, rhs))

	return table[::-1], {j: i for i, j in enumerate(indices)}

def solve_matrix(matrix, x_max):
	best = []
	best_sum = sum(x_max) + 1
	table, index_map = make_table(matrix, x_max)
	mul = operator.mul

	def recurse(y, x_sum, x):
		nonlocal best_sum
		can_break, entries, x_max, fixed, rhs = table[y]
		rhs -= sum(map(mul, fixed, x))

		for x_sum, values in gen_values(x_max, x_sum):
			if x_sum >= best_sum: break
			lhs = sum(map(mul, values, entries))
			if lhs != rhs:
				if can_break and lhs > rhs: break
			elif y:
				recurse(y-1, x_sum, x + values)
			elif x_sum < best_sum:
				best[:] = x + values
				best_sum = x_sum

	recurse(len(matrix)-1, 0, ())
	return [best[index_map[i]] for i in range(len(x_max))]

def solve2(machine, machine_num):
	buttons, joltages = machine
	max_presses = [min(joltages[i] for i in b) for b in buttons]
	matrix = [[int(i in b) for b in buttons] + [j] for i, j in enumerate(joltages)]

	scipy_result = solve2_scipy(machine, full_result=True)
	scipy_result = list(map(round, scipy_result.x))
	scipy_result_sum = sum(scipy_result)

	reduce_matrix(matrix)
	result = solve_matrix(matrix, max_presses)
	result_sum = sum(result)

	assert check_result(buttons, joltages, scipy_result)
	assert check_result(buttons, joltages, result)
	assert result_sum == scipy_result_sum

#	if result != scipy_result:
#		print('Machine', machine_num)
#		print_result(result)
#		print_result(scipy_result)
	return result_sum

def main(f):
	pattern = re.compile(r'^\[[#.]+\](?: \(\d(?:,\d)*\))+ \{\d+(?:,\d+)*\}$')
	machines1 = []
	machines2 = []
	for line_num, line in enumerate(f, start=1):
		if not pattern.match(line):
			return f'Line {line_num} doesn\'t match the expected pattern!'
		lights, *buttons, joltages = line.split()
		lights = sum(1 << i for i, light in enumerate(lights[1:-1]) if light == '#')
		buttons = [[int(i) for i in button[1:-1].split(',')] for button in buttons]
		joltages = [int(i) for i in joltages[1:-1].split(',')]
		machines1.append((buttons, lights))
		machines2.append((buttons, joltages))

	print('Part 1:', sum(map(solve1, machines1)))
#	print('Part 2:', sum(map(solve2_scipy, machines2)))
	print('Part 2:', sum(map(solve2, machines2, range(len(machines2)))))

if __name__ == '__main__':
	sys.exit(main(sys.stdin))

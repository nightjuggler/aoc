import sys

def get_op_modes(number):
	number, op = divmod(number, 100)
	modes = []
	while number:
		number, mode = divmod(number, 10)
		assert mode <= 2
		modes.append(mode)
	return op, modes

def run(program, inputs):
	program = program.copy()
	inputs = iter(inputs)
	outputs = []
	i = relative_base = 0

	def get_args(n, store_last=False):
		nonlocal i
		if (mlen := len(modes)) < n:
			modes.extend([0] * (n - mlen))
		else:
			assert mlen == n
		for j, mode in enumerate(modes, start=1):
			arg = program.get(i+j, 0)
			if mode != 1:
				if mode == 2:
					arg += relative_base
				assert arg >= 0
				if not (store_last and j == n):
					arg = program.get(arg, 0)
			else:
				assert not (store_last and j == n)
			yield arg
		i += n + 1

	def op_add(a, b): return a + b
	def op_mul(a, b): return a * b
	def op_lss(a, b): return int(a < b)
	def op_eql(a, b): return int(a == b)

	def op3(fn):
		a, b, c = get_args(3, True)
		program[c] = fn(a, b)

	while True:
		op, modes = get_op_modes(program.get(i, 0))
		if   op == 1: op3(op_add)
		elif op == 2: op3(op_mul)
		elif op == 3: # -------------------- INPUT
			a, = get_args(1, True)
			program[a] = next(inputs)
		elif op == 4: # -------------------- OUTPUT
			a, = get_args(1)
			outputs.append(a)
		elif op == 5: # -------------------- JUMP-IF-TRUE
			a, b = get_args(2)
			if a: i = b
		elif op == 6: # -------------------- JUMP-IF-FALSE
			a, b = get_args(2)
			if not a: i = b
		elif op == 7: op3(op_lss)
		elif op == 8: op3(op_eql)
		elif op == 9: # -------------------- ADJUST-RELATIVE-BASE
			a, = get_args(1)
			relative_base += a
		elif op == 99:
			break
		else:
			sys.exit(f'Unknown opcode {op} at position {i}!')
	return outputs

def print_beam(program, x_range, y_range):
	for y in y_range:
		print(''.join(['.#'[run(program, [x, y])[0]] for x in x_range]))

def part_one(program, size):
	return sum(run(program, [x, y])[0]
		for y in range(size)
		for x in range(size))

def part_two(program, size):
	if size == 1: return 0
	for y in range(size, 10_000):
		for x in range(y, -1, -1):
			if run(program, [x,y])[0] != 0: break
		else:
			print(f'No beam between 0,{y} and {y},{y}!')
			continue
		x -= size - 1
		y2 = y + size - 1
		if run(program, [x,y])[0] == 0: continue
		if run(program, [x,y2])[0] == 0: continue
		while True:
			if run(program, [x-1,y])[0] == 0: break
			if run(program, [x-1,y2])[0] == 0: break
			x -= 1
		assert run(program, [x+size-1,y2])[0] != 0
		return x*10_000 + y
	return None

def main():
	program = dict(enumerate(map(int, sys.stdin.readline().split(','))))

	print('Part 1:', part_one(program, 50))
	print('Part 2:', part_two(program, 100))

if __name__ == '__main__':
	main()

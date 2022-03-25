import sys

def get_op_modes(number):
	number, op = divmod(number, 100)
	modes = []
	while number:
		number, mode = divmod(number, 10)
		assert mode <= 2
		modes.append(mode)
	return op, modes

def run(program, part2=False):
	program = program.copy()
	if part2: program[0] = 2
	i = relative_base = 0
	outputs = []
	score = None
	ball_x = None
	ball_y = None
	ball_dx = 0
	paddle_x = None
	paddle_y = None
	grid = {}

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
			b = ball_x + ball_dx * (paddle_y - 1 - ball_y) - paddle_x
			if b: b //= abs(b)
			program[a] = b
		elif op == 4: # -------------------- OUTPUT
			a, = get_args(1)
			outputs.append(a)
			if len(outputs) == 3:
				x, y, tile = outputs
				outputs.clear()
				if not part2:
					assert x >= 0 and y >= 0
					assert 0 <= tile <= 4
					grid[x, y] = tile
					continue
				if x < 0 == y:
					score = tile
					continue
				assert x >= 0 and y >= 0
				assert 0 <= tile <= 4
				if tile == 4:
					if ball_x is not None: ball_dx = x - ball_x
					assert -1 <= ball_dx <= 1
					ball_x = x
					ball_y = y
				elif tile == 3:
					paddle_x = x
					paddle_y = y
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

	return score if part2 else sum(tile == 2 for tile in grid.values())

def main():
	with open('data/13.input') as f:
		program = dict(enumerate(map(int, f.readline().split(','))))

	print('Part 1:', run(program))
	print('Part 2:', run(program, part2=True))

if __name__ == '__main__':
	main()

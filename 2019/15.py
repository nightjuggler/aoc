from collections import deque
import sys

def get_op_modes(number):
	number, op = divmod(number, 100)
	modes = []
	while number:
		number, mode = divmod(number, 10)
		assert mode <= 2
		modes.append(mode)
	return op, modes

def run(program):
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
			program[a] = yield None
		elif op == 4: # -------------------- OUTPUT
			a, = get_args(1)
			yield a
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

def print_grid(grid):
	min_x = max_x = 0
	min_y = max_y = 0
	for x, y in grid:
		if   x < min_x: min_x = x
		elif x > max_x: max_x = x
		if   y < min_y: min_y = y
		elif y > max_y: max_y = y
	print(f'x={min_x}..{max_x}, y={min_y}..{max_y}')
	for y in range(min_y, max_y + 1):
		print(''.join(['#.O '[grid.get((x, y), 3)] for x in range(min_x, max_x + 1)]))

def discover(program):
	x = y = 0
	grid = {(0, 0): 1}
	move = 1 # 1=north, 2=south, 3=west, 4=east
	xy = (0, -1)
	path = []

	while True:
		try:
			output = program.send(None)
		except StopIteration:
			sys.exit('Unexpected end of program!')
		assert output is None

		try:
			output = program.send(move)
		except StopIteration:
			sys.exit('Unexpected end of program!')
		assert 0 <= output <= 2

		if xy in grid:
			assert grid[xy] == output != 0
			x, y = xy
			move = (0, 2, 1, 4, 3)[move] + 1
		else:
			grid[xy] = output
			if output:
				x, y = xy
				path.append(move)
				move = 1
			else:
				move += 1

		while move <= 4:
			xy = (
				(x, y-1) if move == 1 else
				(x, y+1) if move == 2 else
				(x-1, y) if move == 3 else
				(x+1, y))
			if xy not in grid: break
			move += 1
		else:
			if not path: break
			move = (0, 2, 1, 4, 3)[path.pop()]
			xy = (
				(x, y-1) if move == 1 else
				(x, y+1) if move == 2 else
				(x-1, y) if move == 3 else
				(x+1, y))
	return grid

def part1(grid):
	q = deque()
	q.append((0, 0, 0))
	grid[0, 0] = 0

	while q:
		step, x, y = q.popleft()
		step += 1
		for xy in (x, y+1), (x+1, y), (x, y-1), (x-1, y):
			if o := grid[xy]:
				if o == 2: return step
				q.append((step, *xy))
				grid[xy] = 0
	return None

def part2(grid):
	xy = [xy for xy, o in grid.items() if o == 2]
	assert len(xy) == 1
	xy = xy.pop()

	q = deque()
	q.append((0, *xy))
	grid[xy] = 0

	while q:
		step, x, y = q.popleft()
		step += 1
		for xy in (x, y+1), (x+1, y), (x, y-1), (x-1, y):
			if o := grid[xy]:
				q.append((step, *xy))
				grid[xy] = 0
	return step-1

def main():
	with open('data/15.input') as f:
		program = dict(enumerate(map(int, f.readline().split(','))))

	grid = discover(run(program))
#	print_grid(grid)
	print('Part 1:', part1(grid.copy()))
	print('Part 2:', part2(grid))

if __name__ == '__main__':
	main()

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

def get_moves(robot, facing, scaffold, intersections):
	x, y = robot
	adjacent = (x, y-1), (x+1, y), (x, y+1), (x-1, y)
	scaffold_ahead, scaffold_right, scaffold_behind, scaffold_left = [
		adjacent[(facing + i) % 4] in scaffold for i in range(4)]
	assert not scaffold_ahead
	assert not scaffold_behind
	moves = []
	if scaffold_right:
		assert not scaffold_left
		moves.append('R')
		facing = (facing + 1) % 4
	else:
		assert scaffold_left
		moves.append('L')
		facing = (facing + 3) % 4
	steps = 1
	while True:
		x, y = robot = adjacent[facing]
		visits = scaffold[robot]
		scaffold[robot] = visits + 1
		adjacent = (x, y-1), (x+1, y), (x, y+1), (x-1, y)
		if robot in intersections:
			assert visits <= 1
			steps += 1
		elif adjacent[facing] in scaffold:
			assert visits == 0
			steps += 1
		else:
			assert visits == 0
			moves.append(str(steps))
			right = (facing + 1) % 4
			left = (facing + 3) % 4
			if adjacent[right] in scaffold:
				moves.append('R')
				facing = right
			elif adjacent[left] in scaffold:
				moves.append('L')
				facing = left
			else:
				break
			steps = 1
	for xy, visits in scaffold.items():
		assert visits == (2 if xy in intersections else 1)
	return ','.join(moves)

def chunkify(moves, max_chunk_len, max_num_chunks):
	chunks = []

	def _chunkify(parts):
		s = parts[0]
		if (i := len(s)) > max_chunk_len:
			i = s.rfind(',', 0, max_chunk_len+1)
		while i > 0:
			s = s[:i]
			chunks.append(s)
			s_with_commas = ',' + s + ','
			parts_left = [q for q in [q.strip(',') for p in parts
				for q in (',' + p + ',').split(s_with_commas)] if q]
			if not parts_left:
				return True
			if len(chunks) < max_num_chunks and _chunkify(parts_left):
				return True
			chunks.pop()
			i = s.rfind(',')
		return False

	_chunkify([moves])
	return chunks

def part2(program, robot_and_scaffold):
	moves = get_moves(*robot_and_scaffold)

	chunks = chunkify(moves, 20, 3)
	assert chunks
	for i, chunk in enumerate(chunks):
		moves = moves.replace(chunk, chr(ord('A') + i))
	if len(chunks) < 3:
		chunks.extend([''] * (3 - len(chunks)))

	inputs = '\n'.join([moves, *chunks, 'n', ''])
#	print(inputs)
	inputs = list(map(ord, inputs))

	assert program[0] == 1
	program[0] = 2
	output = run(program, inputs)
	dust = output.pop()
#	print(''.join(map(chr, output)).rstrip('\n'))
	print('Part 2:', dust)

def part1(program):
	output = run(program, [])
	valid_chars = set(map(ord, '\n#.<>^v'))
	assert all(c in valid_chars for c in output)
	output = ''.join(map(chr, output)).rstrip('\n')
#	print(output)

	robot = None
	facing = None
	scaffold = {}
	for y, line in enumerate(output.split('\n')):
		for x, c in enumerate(line):
			if c == '#':
				scaffold[x, y] = 0
			elif c != '.':
				assert robot is None
				robot = x, y
				facing = '^>v<'.index(c)
	intersections = set()
	for x, y in scaffold:
		n = sum(xy in scaffold for xy in ((x, y-1), (x+1, y), (x, y+1), (x-1, y)))
		if n == 4:
			intersections.add((x, y))
		else:
			assert n == 2 or n == 1

	print('Part 1:', sum(x * y for x, y in intersections))
	return robot, facing, scaffold, intersections

def main():
	program = dict(enumerate(map(int, sys.stdin.readline().split(','))))
	robot_and_scaffold = part1(program)
	part2(program, robot_and_scaffold)

if __name__ == '__main__':
	main()

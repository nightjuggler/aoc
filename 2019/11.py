import sys

def get_op_modes(number):
	number, op = divmod(number, 100)
	modes = []
	while number:
		number, mode = divmod(number, 10)
		assert mode <= 2
		modes.append(mode)
	return op, modes

def run(program, white):
	program = program.copy()
	i = relative_base = 0
	x = y = 0
	move_up_down = True
	move_delta = -1
	state = 2
	painted = set()

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
			if state != 2:
				sys.exit('Expected output instead of input!')
			state = 0
			a, = get_args(1, True)
			program[a] = int((x, y) in white)
		elif op == 4: # -------------------- OUTPUT
			a, = get_args(1)
			assert a == 0 or a == 1
			if state == 0:
				state = 1
				xy = (x, y)
				painted.add(xy)
				if a:
					white.add(xy)
				else:
					white.discard(xy)
			elif state == 1:
				state = 2
				# if a == 0: turn left
				# if a == 1: turn right
				if move_up_down == a:
					move_delta = -move_delta
				if move_up_down := not move_up_down:
					y += move_delta
				else:
					x += move_delta
			else:
				sys.exit('Expected input instead of output!')
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
	return len(painted)

def main():
	program = dict(enumerate(map(int, sys.stdin.readline().split(','))))

	white = set()
	print('Part 1:', run(program, white))
	print('Part 2:')
	white = {(0, 0)}
	run(program, white)
	if not white: return

	x, y = white.pop()
	min_x = max_x = x
	min_y = max_y = y
	white.add((x, y))

	for x, y in white:
		if   x < min_x: min_x = x
		elif x > max_x: max_x = x
		if   y < min_y: min_y = y
		elif y > max_y: max_y = y

	for y in range(min_y, max_y + 1):
		print(''.join([' #'[(x, y) in white] for x in range(min_x, max_x + 1)]))

if __name__ == '__main__':
	main()

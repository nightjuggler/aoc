import curses
import sys
import time

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
	output = []

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
			assert not output
			a, = get_args(1, True)
			program[a] = yield None
		elif op == 4: # -------------------- OUTPUT
			a, = get_args(1)
			output.append(a)
			if len(output) == 3:
				yield output
				output.clear()
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

def play(program, stdscr):
	program[0] = 2
	program = run(program)

	max_x = 0
	max_y = 0
	ball_x = None
	ball_y = None
	ball_dx = 0
	paddle_x = None
	paddle_y = None
	grid = {}
	num_blocks = 0

	curses.curs_set(0)
	stdscr.clear()
	stdscr.timeout(0) # non-blocking read

	for x, y, tile in program:
		if x < 0:
			assert y == 0 == tile
			break

		assert y >= 0
		if x > max_x: max_x = x
		if y > max_y: max_y = y

		assert (x, y) not in grid
		grid[x, y] = tile
		stdscr.addch(y, x, ' |#=o'[tile])

		if tile <= 1: continue
		if tile == 2:
			num_blocks += 1
		elif tile == 3:
			assert paddle_x is None
			paddle_x = x
			paddle_y = y
		elif tile == 4:
			assert ball_x is None
			ball_x = x
			ball_y = y

	max_x += 1
	max_y += 1
	assert len(grid) == max_x * max_y
	score = 0
	stdscr.addstr(max_y, 0, 'Score: 0')
	blocks = num_blocks
	blocks_str = f'{blocks:,} Blocks'
	blocks_x = max_x - len(blocks_str)
	blocks_spec = str(max_x - blocks_x - 7) + ','
	stdscr.addstr(max_y, blocks_x, blocks_str)
	stdscr.refresh()
	send_value = None
	autoplay = True
	delay = 1
	quit = False

	while True:
		try:
			output = program.send(send_value)
		except StopIteration:
			break
		if output:
			send_value = None
			x, y, tile = output
			if x < 0:
				assert y == 0 <= tile
				score = tile
				stdscr.addstr(max_y, 0, f'Score: {score:<6,}')
				stdscr.refresh()
				continue

			prev = grid[x, y]
			grid[x, y] = tile
			stdscr.addch(y, x, ' |#=o'[tile])

			if tile == 0:
				if prev == 2:
					blocks -= 1
					stdscr.addstr(max_y, blocks_x, format(blocks, blocks_spec))
			elif tile == 4:
				ball_dx = x - ball_x
				ball_x = x
				ball_y = y
			elif tile == 3:
				paddle_x = x
				assert y == paddle_y
			else:
				sys.exit("Unexpected tile ({' |#=o'[tile]}) during play!")
		else:
			stdscr.refresh()
			if (c := stdscr.getch()) > 0:
				c = chr(c)
				if c == 'q':
					quit = True
					break
				elif c == ',': delay = min(100, delay+1)
				elif c == '.': delay = max(1, delay-1)
				elif c == '[': delay = min(100, delay+10)
				elif c == ']': delay = max(1, delay-10)
				elif c == 'm':
					autoplay = not autoplay
					stdscr.timeout(0 if autoplay else -1)
			if autoplay:
				time.sleep(delay / 100)
				send_value = ball_x + ball_dx * (paddle_y - 1 - ball_y) - paddle_x
				if send_value:
					send_value //= abs(send_value)
			else:
				while c not in 'jkl': c = stdscr.getkey()
				send_value = ord(c) - ord('k')

	stdscr.timeout(-1) # blocking read
	if not quit:
		while stdscr.getkey() != 'q': pass

	return num_blocks, score

def main():
	with open('data/13.input') as f:
		program = dict(enumerate(map(int, f.readline().split(','))))

	def play_wrapper(stdscr):
		return play(program, stdscr)

	num_blocks, score = curses.wrapper(play_wrapper)

	print('Part 1:', num_blocks)
	print('Part 2:', score)

if __name__ == '__main__':
	main()

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

def run(program, addr, queues):
	idle = 0
	clock = None
	output = []
	input_q = queues[addr]
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
			if input_q:
				program[a] = input_q.popleft()
				idle = 0
			else:
				program[a] = -1
				idle += 1
			if not clock:
				yield (idle,)
				clock = 1
				continue
		elif op == 4: # -------------------- OUTPUT
			a, = get_args(1)
			output.append(a)
			if len(output) == 3:
				dest, x, y = output
				output.clear()
				idle = 0
				if dest < 50:
					q = queues[dest]
					q.append(x)
					q.append(y)
				elif dest == 255:
					yield (idle, x, y)
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
		if clock:
			if clock == 20:
				yield (idle,)
				clock = 1
			else:
				clock += 1
	return None

def main():
	with open('data/23.input') as f:
		program = dict(enumerate(map(int, f.readline().split(','))))

	nat_xy = None
	nat_ysent = set()
	queues = []
	programs = []

	for addr in range(50):
		q = deque()
		q.append(addr)
		queues.append(q)
		programs.append(run(program.copy(), addr, queues))

	while programs:
		running = []
		all_idle = True
		for program in programs:
			try:
				idle, *xy = program.send(None)
			except StopIteration:
				continue
			running.append(program)
			if idle < 2:
				all_idle = False
			if xy:
				if not nat_xy:
					print('Part 1:', xy[1])
				nat_xy = xy
		programs = running
		if all_idle:
			queues[0].extend(nat_xy)
			y = nat_xy[1]
			if y in nat_ysent:
				print('Part 2:', y)
				return
			nat_ysent.add(y)
main()

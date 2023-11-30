from collections import deque
import re
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
	output = []
	input_q = deque()
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
			if not input_q:
				input_q.extend((yield ''.join(output)))
				output.clear()
			program[a] = ord(input_q.popleft())
		elif op == 4: # -------------------- OUTPUT
			a, = get_args(1)
			output.append(chr(a))
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
	return ''.join(output)

class UnexpectedOutput(Exception):
	pass

def play_interactive(program):
	while True:
		command = input()
		try:
			output = program.send(command + '\n')
		except StopIteration as e:
			print(e.value.rstrip())
			break
		print(output.rstrip())

def main():
	with open('data/25.input') as f:
		program = dict(enumerate(map(int, f.readline().split(','))))
	program = run(program)

	room_pattern = re.compile('^\\n\\n\\n'
		'== ([A-Z][a-z]+(?: [A-Z][a-z]+)*) ==\\n'
		'[- \',.0-9:;?A-Za-z]+\\n\\n'
		'Doors here lead:\\n((?:- [a-z]+\\n)+)\\n'
		'(?:Items here:\\n((?:-(?: [a-z]+)+\\n)+)\\n)?'
		'Command\\?$')
	do_not_take = (
		'escape pod',
		'giant electromagnet',
		'infinite loop',
		'molten lava',
		'photons',
	)
	move_back = {
		'north\n': 'south\n',
		'south\n': 'north\n',
		'east\n': 'west\n',
		'west\n': 'east\n',
	}
	inventory = []
	checkpoint_path = None

	def take(item, drop=False):
		command = 'drop' if drop else 'take'
		try:
			output = program.send(f'{command} {item}\n')
		except StopIteration as e:
			print(e.value)
			sys.exit('Program ended!')
		if output != f'\nYou {command} the {item}.\n\nCommand?\n':
			print(output)
			raise UnexpectedOutput()

	def move(door):
		try:
			output = program.send(door)
		except StopIteration as e:
			print(e.value)
			sys.exit('Program ended!')
		m = room_pattern.match(output)
		if not m:
			print(output)
			raise UnexpectedOutput()
		room, doors, items = m.groups()
		doors = doors.split('- ')[1:]
		items = items.split('- ')[1:] if items else []
		return room, doors, items

	def explore(path):
		nonlocal checkpoint_path
		if path:
			door = path[-1]
			back = move_back[door]
		else:
			door = back = None
		room, doors, items = move(door)
		for item in items:
			item = item[:-1]
			if item not in do_not_take:
				take(item)
				inventory.append(item)
		if room == 'Security Checkpoint':
			checkpoint_path = path.copy()
		else:
			for door in doors:
				if door != back:
					path.append(door)
					explore(path)
					path.pop()
		if back:
			move(back)

	def check_move():
		x1 = (
			'\n\n\n== Pressure-Sensitive Floor ==\n'
			'Analyzing...\n\n'
			'Doors here lead:\n- north\n\n'
		)
		x2 = x1 + 'A loud, robotic voice says "Alert! Droids on this ship are '
		x3 = (
			' than the detected value!" and you are ejected back to the checkpoint.\n'
			'\n\n\n== Security Checkpoint ==\n'
		)
		try:
			output = program.send('south\n')
		except StopIteration as e:
			sys.exit(e.value.removeprefix(x1).rstrip())

		i = len(x2)
		j = i + len('lighter') # len('lighter') == len('heavier')
		k = j + len(x3)
		s = output[i:j]

		if not (output[:i] == x2
			and (s == 'lighter' or s == 'heavier')
			and output[j:k] == x3
		):
			print(output)
			raise UnexpectedOutput()

		return s == 'lighter'

	def combine(taken, remaining):
		if check_move(): return
		for i, item in enumerate(remaining):
			take(item)
			taken.append(item)
			combine(taken, remaining[i+1:])
			take(item, drop=True)
			taken.pop()

	try:
		explore([])
		# Move back to the security checkpoint, and drop all items.
		for door in checkpoint_path:
			move(door)
		for item in inventory:
			take(item, drop=True)
		combine([], inventory)
	except UnexpectedOutput:
		pass

	play_interactive(program)
main()

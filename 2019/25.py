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

def main():
	with open('data/25.input') as f:
		program = dict(enumerate(map(int, f.readline().split(','))))
	program = run(program)

	floor_description = (
		'\n\n\n== Pressure-Sensitive Floor ==\n'
		'Analyzing...\n\n'
		'Doors here lead:\n- north\n\n'
	)
	check_fail_pattern = re.compile('Droids on this ship are (heavier|lighter) than the detected value')
	check_pass_pattern = re.compile('You should be able to get in by typing ([0-9]+) on the keypad')
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
		'north': 'south',
		'south': 'north',
		'east': 'west',
		'west': 'east',
	}
	inventory = []
	checkpoint_path = None

	def take(item, drop=False):
		command = 'drop' if drop else 'take'
		try:
			output = program.send(f'{command} {item}\n')
		except StopIteration as e:
			sys.exit(e.value.strip())
		if output != f'\nYou {command} the {item}.\n\nCommand?\n':
			sys.exit(output.strip())

	def move(door):
		if door: door += '\n'
		try:
			output = program.send(door)
		except StopIteration as e:
			sys.exit(e.value.strip())
		m = room_pattern.match(output)
		if not m:
			sys.exit(output.strip())
		room, doors, items = m.groups()
		doors = doors.strip('\n- ').split('\n- ')
		items = items.strip('\n- ').split('\n- ') if items else []
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
			if item not in do_not_take:
				take(item)
				inventory.append(item)
		if room == 'Security Checkpoint':
			assert door == 'south' and doors == ['north', 'south']
			checkpoint_path = path.copy()
		else:
			for door in doors:
				if door != back:
					path.append(door)
					explore(path)
					path.pop()
		if back:
			move(back)

	def check_weight():
		try:
			output = program.send('south\n')
			pattern = check_fail_pattern
		except StopIteration as e:
			output = e.value
			pattern = check_pass_pattern

		if not output.startswith(floor_description):
			sys.exit(output.strip())
		m = pattern.search(output.removeprefix(floor_description))
		if not m:
			sys.exit(output.strip())
		value = m.group(1)
		if pattern is check_pass_pattern:
			print('The password is', value)
			return 0
		return -1 if value == 'lighter' else 1

	def combine(taken, remaining):
		cmp = check_weight()
		if cmp == 0: return True
		if cmp < 0: return False
		for i, item in enumerate(remaining):
			take(item)
			taken.append(item)
			if combine(taken, remaining[i+1:]):
				return True
			take(item, drop=True)
			taken.pop()
		return False

	explore([])
	# Move back to the security checkpoint, and drop all items.
	for door in checkpoint_path:
		move(door)
	for item in inventory:
		take(item, drop=True)
	combine([], inventory)
main()

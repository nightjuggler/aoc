import sys

err = sys.exit

def read_with_spec(f, i, spec):
	values = []
	for (prefix, suffix, is_valid, get_value), (i, line) in zip(spec, enumerate(f, start=i+1)):
		line = line.strip()
		if not (line.startswith(prefix) and line.endswith(suffix)):
			err(f'Line {i} doesn\'t match spec!')
		value = line[len(prefix):-len(suffix)]
		if not is_valid(value):
			err(f'Line {i} value doesn\'t match spec!')
		values.append(get_value(value))
	if len(values) != len(spec):
		err(f'Line {i+1} doesn\'t match spec!')
	return [x for x in values if x is not None], i+1

def read_input(f):
	states = []

	def check_S(x): return len(x) == 1 and len(states) == ord(x) - 65 < 26
	def check_0(x): return x == '0'
	def check_1(x): return x == '1'
	def check_W(x): return x == '0' or x == '1'
	def check_M(x): return x == 'left' or x == 'right'
	def check_L(x): return len(x) == 1 and 65 <= ord(x) <= 90
	def check_I(x): return x and all(48 <= ord(d) <= 57 for d in x) and x[0] != '0'

	def value_W(x): return x == '1'
	def value_M(x): return -1 if x == 'left' else 1
	def value_L(x): return ord(x) - 65
	def value_I(x): return int(x)
	def value_N(x): return None

	spec = (
		('Begin in state ', '.', check_L, value_L),
		('Perform a diagnostic checksum after ', ' steps.', check_I, value_I),
	)
	config, i = read_with_spec(f, 0, spec)

	spec_W = ('- Write the value ',      '.', check_W, value_W)
	spec_M = ('- Move one slot to the ', '.', check_M, value_M)
	spec_L = ('- Continue with state ',  '.', check_L, value_L)
	spec = (
		('In state ',                ':', check_S, value_N),
		('If the current value is ', ':', check_0, value_N), spec_W, spec_M, spec_L,
		('If the current value is ', ':', check_1, value_N), spec_W, spec_M, spec_L,
	)
	for line in f:
		if line.strip():
			err(f'Line {i} expected to be blank!')
		values, i = read_with_spec(f, i, spec)
		states.append((values[:3], values[3:]))

	return config, states

def main():
	(state0, steps), states = read_input(sys.stdin)

	for if0, if1 in states:
		if0[2] = states[if0[2]]
		if1[2] = states[if1[2]]
	x = 0
	ones = set()
	state = states[state0]

	for _ in range(steps):
		old_value = x in ones
		new_value, dx, state = state[old_value]
		if old_value != new_value:
			if new_value:
				ones.add(x)
			else:
				ones.remove(x)
		x += dx

	print(len(ones))
main()

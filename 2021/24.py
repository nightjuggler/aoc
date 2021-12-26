import re
import sys

def op_add(a, b): return f'{a} += {b}'
def op_mul(a, b): return f'{a} *= {b}'
def op_div(a, b): return f'{a} //= {b}' # f'{a} = int({a} / {b})'
def op_mod(a, b): return f'{a} %= {b}'
def op_eql(a, b): return f'{a} = int({a} == {b})'
def op_neq(a, b): return f'{a} = int({a} != {b})'
def op_set(a, b): return f'{a} = {b}'
def op_set2(a, args): return ' '.join([a, '=', *args])

instructions = {
	'add': op_add,
	'mul': op_mul,
	'div': op_div,
	'mod': op_mod,
	'eql': op_eql,
}

class InputError(Exception):
	pass

def read_input():
	line_pattern = re.compile('^[a-z]{3} [wxyz](?: (?:[wxyz]|0|-?[1-9][0-9]*))?$')
	program = []
	section = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			raise InputError(f'Input line {line_num} doesn\'t match pattern!')
		op, *args = line.split()
		if op == 'inp':
			if len(args) != 1:
				raise InputError(f'Input line {line_num}: Expected one argument!')
			if args[0] != 'w':
				raise InputError(f"Input line {line_num}: Expected 'w' with 'inp'!")
			program.append(section)
			section = []
			continue
		if len(args) != 2:
			raise InputError(f'Input line {line_num}: Expected two arguments!')
		arg0, arg1 = args
		if op == 'div' and arg1 == '1':
			continue
		if section and (prev := section[-1])[1] == arg0:
			prev_op, prev_arg = prev[0], prev[2]
			if prev_op is op_mul:
				if op == 'add' and prev_arg == '0':
					section[-1] = (op_set, arg0, arg1)
					continue
			elif prev_op is op_set:
				op_arg = (
					'+' if op == 'add' else
					'*' if op == 'mul' else
					'%' if op == 'mod' else None)
				if op_arg:
					section[-1] = (op_set2, arg0, [prev_arg, op_arg, arg1])
					continue
			elif prev_op is op_set2:
				if op == 'add':
					prev_arg.extend(('+', arg1))
					continue
				if op == 'mul':
					prev_arg[:] = ['({})'.format(' '.join(prev_arg)), '*', arg1]
					continue
			elif prev_op is op_eql:
				if op == 'eql' and arg1 == '0':
					section[-1] = (op_neq, arg0, prev_arg)
					continue
		fn = instructions.get(op)
		if not fn:
			raise InputError(f'Input line {line_num}: Unknown instruction!')
		section.append((fn, arg0, arg1))
	program.append(section)
	return program

def main():
	try:
		program = read_input()
	except InputError as e:
		print(e)
		return

	for n, section in enumerate(program):
		print(f'def section{n}(w, z):')
		for fn, *args in section:
			print('\t', fn(*args), sep='')
		print('\treturn z\n')

	print('sections = [')
	for n in range(len(program)):
		print('\t', 'section', n, ',', sep='')
	print(']')

	print(f'''
def main():
	seen = set()
	digits = range(9, 0, -1)
	answer = []

	def solve(depth, w, z):
		z = sections[depth](w, z)

		if depth == {n}:
			return z == 0

		state = (depth, z)
		if state in seen:
			return False

		for w in digits:
			if solve(depth + 1, w, z):
				answer.append(w)
				return True

		seen.add(state)
		return False

	solve(0, 0, 0)
	answer.reverse()
	print('Part 1: ', *answer, sep='')

	answer.clear()
	digits = range(1, 10)
	solve(0, 0, 0)
	answer.reverse()
	print('Part 2: ', *answer, sep='')

main()''')

if __name__ == '__main__':
	main()

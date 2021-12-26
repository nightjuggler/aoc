import re
import sys

# This is a slower solution that interprets the puzzle input code rather than
# converting it to Python. It takes about 23 seconds to find the answer to part 1
# and an additional 9 minutes plus a few seconds to find the answer to part 2.

def op_addi(r, a, b): r[a] += b
def op_addr(r, a, b): r[a] += r[b]

def op_muli(r, a, b): r[a] *= b
def op_mulr(r, a, b): r[a] *= r[b]

def op_divi(r, a, b): r[a] //= b
def op_divr(r, a, b): r[a] //= r[b]

# def op_divi(r, a, b): r[a] = int(r[a] / b)
# def op_divr(r, a, b): r[a] = int(r[a] / r[b])

def op_modi(r, a, b): r[a] %= b
def op_modr(r, a, b): r[a] %= r[b]

def op_eqli(r, a, b): r[a] = int(r[a] == b)
def op_eqlr(r, a, b): r[a] = int(r[a] == r[b])
def op_neqr(r, a, b): r[a] = int(r[a] != r[b])

# def op_eqli(r, a, b): r[a] = 1 if r[a] == b else 0
# def op_eqlr(r, a, b): r[a] = 1 if r[a] == r[b] else 0
# def op_neqr(r, a, b): r[a] = 1 if r[a] != r[b] else 0

def op_seti(r, a, b): r[a] = b
def op_setr(r, a, b): r[a] = r[b]

instructions = {
	'addi': op_addi,
	'addr': op_addr,
	'muli': op_muli,
	'mulr': op_mulr,
	'divi': op_divi,
	'divr': op_divr,
	'modi': op_modi,
	'modr': op_modr,
	'eqli': op_eqli,
	'eqlr': op_eqlr,
}

class InputError(Exception):
	pass

def read_input():
	line_pattern = re.compile('^[a-z]{3} [wxyz](?: (?:[wxyz]|0|-?[1-9][0-9]*))?$')
	program = []
	for line_num, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			raise InputError(f'Input line {line_num} doesn\'t match pattern!')
		op, *args = line.split()
		arg0 = ord(args[0]) - ord('w')
		if op == 'inp':
			if len(args) != 1:
				raise InputError(f'Input line {line_num}: Expected one argument!')
			program.append((None, arg0, None))
			continue
		if len(args) != 2:
			raise InputError(f'Input line {line_num}: Expected two arguments!')
		arg1 = args[1]
		if arg1 in 'wxyz':
			arg1 = ord(arg1) - ord('w')
			if op == 'add' and program and program[-1] == (op_muli, arg0, 0):
				program[-1] = (op_setr, arg0, arg1)
				continue
			op += 'r'
		else:
			arg1 = int(arg1)
			if op == 'div' and arg1 == 1:
				continue
			if program and (prev := program[-1])[1] == arg0:
				prev_op, prev_arg = prev[0], prev[2]
				if op == 'add' and prev_op is op_muli and prev_arg == 0:
					program[-1] = (op_seti, arg0, arg1)
					continue
				if op == 'eql' and arg1 == 0 and prev_op is op_eqlr:
					program[-1] = (op_neqr, arg0, prev_arg)
					continue
			op += 'i'
		fn = instructions.get(op)
		if not fn:
			raise InputError(f'Input line {line_num}: Unknown instruction!')
		program.append((fn, arg0, arg1))
	return program

def main():
	try:
		program = read_input()
	except InputError as e:
		print(e)
		return

	seen = set()
	digits = range(9, 0, -1)
	answer = []
	proglen = len(program)

	def solve(i, reg):
		for i in range(i, proglen):
			fn, a, b = program[i]
			if fn:
				fn(reg, a, b)
			else:
				state = (i, *reg)
				if state in seen:
					return False
				for digit in digits:
					reg[a] = digit
					if solve(i + 1, reg.copy()):
						answer.append(digit)
						return True
				seen.add(state)
				return False
		return reg[3] == 0

	solve(0, [0, 0, 0, 0])
	answer.reverse()
	print('Part 1: ', *answer, sep='')

	answer.clear()
	digits = range(1, 10)
	solve(0, [0, 0, 0, 0])
	answer.reverse()
	print('Part 2: ', *answer, sep='')

if __name__ == '__main__':
	main()

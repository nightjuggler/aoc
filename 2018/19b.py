import re
import sys

def addr(ip, ip_reg, a, b, c):
	if c == ip_reg:
		if a == c:
			if b == c:
				return f'goto {ip + ip + 1}'
			return f'goto {ip + 1} + reg{b}'
		if b == c:
			return f'goto {ip + 1} + reg{a}'
		return f'goto reg{a} + reg{b} + 1'

	if a == c:
		if b == ip_reg:
			return f'reg{c} += {ip}'
		return f'reg{c} += reg{b}'
	if b == c:
		if a == ip_reg:
			return f'reg{c} += {ip}'
		return f'reg{c} += reg{a}'

	if a == ip_reg:
		if b == ip_reg:
			return f'reg{c} = {ip + ip}'
		return f'reg{c} = {ip} + reg{b}'
	if b == ip_reg:
		return f'reg{c} = {ip} + reg{a}'

	return f'reg{c} = reg{a} + reg{b}'

def addi(ip, ip_reg, a, b, c):
	if c == ip_reg:
		if a == c:
			return f'goto {ip + b + 1}'

		return f'goto reg{a} + {b + 1}'

	if a == c:
		return f'reg{c} += {b}'

	return f'reg{c} = reg{a} + {b}'

def mulr(ip, ip_reg, a, b, c):
	if c == ip_reg:
		if a == c:
			if b == c:
				return f'goto {ip * ip + 1}'
			return f'goto {ip} * reg{b} + 1'
		if b == c:
			return f'goto {ip} * reg{a} + 1'
		return f'goto reg{a} * reg{b} + 1'

	if a == c:
		if b == ip_reg:
			return f'reg{c} *= {ip}'
		return f'reg{c} *= reg{b}'
	if b == c:
		if a == ip_reg:
			return f'reg{c} *= {ip}'
		return f'reg{c} *= reg{a}'

	if a == ip_reg:
		if b == ip_reg:
			return f'reg{c} = {ip * ip}'
		return f'reg{c} = {ip} * reg{b}'
	if b == ip_reg:
		return f'reg{c} = {ip} * reg{a}'

	return f'reg{c} = reg{a} * reg{b}'

def muli(ip, ip_reg, a, b, c):
	if c == ip_reg:
		if a == c:
			return f'goto {ip * b + 1}'

		return f'goto reg{a} * {b} + 1'

	if a == c:
		return f'reg{c} *= {b}'

	return f'reg{c} = reg{a} * {b}'

def bani(ip, ip_reg, a, b, c):
	if c == ip_reg:
		if a == c:
			return f'goto {(ip & b) + 1}'

		return f'goto (reg{a} & {b}) + 1'

	if a == c:
		return f'reg{c} &= {b}'

	return f'reg{c} = reg{a} & {b}'

def bori(ip, ip_reg, a, b, c):
	if c == ip_reg:
		if a == c:
			return f'goto {(ip | b) + 1}'

		return f'goto (reg{a} | {b}) + 1'

	if a == c:
		return f'reg{c} |= {b}'

	return f'reg{c} = reg{a} | {b}'

def setr(ip, ip_reg, a, b, c):
	if c == ip_reg:
		if a == c:
			return f'goto {ip + 1}'
		return f'goto reg{a} + 1'

	if a == ip_reg:
		return f'reg{c} = {ip}'

	return f'reg{c} = reg{a}'

def seti(ip, ip_reg, a, b, c):
	if c == ip_reg:
		return f'goto {a + 1}'

	return f'reg{c} = {a}'

def gtir(ip, ip_reg, a, b, c):
	return f'reg{c} = 1 if {a} > reg{b} else 0'

def gtri(ip, ip_reg, a, b, c):
	return f'reg{c} = 1 if reg{a} > {b} else 0'

def gtrr(ip, ip_reg, a, b, c):
	return f'reg{c} = 1 if reg{a} > reg{b} else 0'

def eqir(ip, ip_reg, a, b, c):
	return f'reg{c} = 1 if {a} == reg{b} else 0'

def eqri(ip, ip_reg, a, b, c):
	return f'reg{c} = 1 if reg{a} == {b} else 0'

def eqrr(ip, ip_reg, a, b, c):
	return f'reg{c} = 1 if reg{a} == reg{b} else 0'

instructions = {
	'addr': addr,
	'addi': addi,
	'mulr': mulr,
	'muli': muli,
	'bani': bani,
	'bori': bori,
	'setr': setr,
	'seti': seti,
	'gtir': gtir,
	'gtri': gtri,
	'gtrr': gtrr,
	'eqir': eqir,
	'eqri': eqri,
	'eqrr': eqrr,
}

def read_input(f):
	line1_pattern = re.compile('^#ip ([012345])$')
	line_pattern = re.compile('^([a-z]{4}) (0|[1-9][0-9]*) (0|[1-9][0-9]*) ([012345])$')
	line_number = 1

	m = line1_pattern.match(f.readline())
	if not m:
		print('Line 1 doesn\'t match expected pattern!')
		return None
	ip_reg = int(m.group(1))

	program = []
	for line in f:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			print(f'Line {line_number} doesn\'t match expected pattern!')
			return None
		op, a, b, c = m.groups()
		fn = instructions.get(op)
		if not fn:
			print(f'Line {line_number}: Unknown instruction!')
			return None
		program.append([op, fn, int(a), int(b), int(c)])

	program.append(ip_reg)
	return program

def main():
	program = read_input(sys.stdin)
	if not program:
		return

	ip_reg = program.pop()

	for ip, (op, fn, a, b, c) in enumerate(program):
		print(f'{ip}:\t', fn(ip, ip_reg, a, b, c), sep='')

if __name__ == '__main__':
	main()

import re
import sys

def addr(reg, a, b): return reg[a] + reg[b]
def addi(reg, a, b): return reg[a] + b
def mulr(reg, a, b): return reg[a] * reg[b]
def muli(reg, a, b): return reg[a] * b
def banr(reg, a, b): return reg[a] & reg[b]
def bani(reg, a, b): return reg[a] & b
def borr(reg, a, b): return reg[a] | reg[b]
def bori(reg, a, b): return reg[a] | b
def setr(reg, a, b): return reg[a]
def seti(reg, a, b): return a
def gtir(reg, a, b): return 1 if a > reg[b] else 0
def gtri(reg, a, b): return 1 if reg[a] > b else 0
def gtrr(reg, a, b): return 1 if reg[a] > reg[b] else 0
def eqir(reg, a, b): return 1 if a == reg[b] else 0
def eqri(reg, a, b): return 1 if reg[a] == b else 0
def eqrr(reg, a, b): return 1 if reg[a] == reg[b] else 0

instructions = {
	'addr': addr,
	'addi': addi,
	'mulr': mulr,
	'muli': muli,
	'banr': banr,
	'bani': bani,
	'borr': borr,
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
	line_pattern = re.compile('^([a-z]{4}) (0|[1-9][0-9]?) (0|[1-9][0-9]?) ([012345])$')
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
	program_len = len(program)
	registers = [0] * 6
	ip = 0

	while ip < program_len:
		op, fn, a, b, c = program[ip]
		registers[ip_reg] = ip
#		print(f'ip={ip}', registers, op, a, b, c, end=' ')
		registers[c] = fn(registers, a, b)
#		print(registers)
		ip = registers[ip_reg] + 1

	print(registers[0])

if __name__ == '__main__':
	main()

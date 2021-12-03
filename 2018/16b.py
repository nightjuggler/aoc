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

instructions = (
	addr, addi, mulr, muli,
	banr, bani, borr, bori,
	setr, seti,
	gtir, gtri, gtrr,
	eqir, eqri, eqrr,
)
instruction_names = (
	'addr', 'addi', 'mulr', 'muli',
	'banr', 'bani', 'borr', 'bori',
	'setr', 'seti',
	'gtir', 'gtri', 'gtrr',
	'eqir', 'eqri', 'eqrr',
)

def make_op2instr(samples):
	op2instr = [None] * len(instructions)

	for before, (op, a, b, c), after in samples:
		before_value = before[c]
		after_value = after[c]
		before[c] = after_value
		if before == after:
			before[c] = before_value
			instrs = [i for i, instr in enumerate(instructions) if instr(before, a, b) == after_value]
		else:
			instrs = []
		if op2instr[op] is None:
			op2instr[op] = set(instrs)
		else:
			op2instr[op].intersection_update(instrs)

	done = False
	for op, instrs in enumerate(op2instr):
		if not instrs:
			print('No possible instruction for opcode', op)
			done = True
	if done:
		return None

	done = [False] * len(op2instr)
	while True:
		remove = set()
		for op, instrs in enumerate(op2instr):
			if len(instrs) == 1 and not done[op]:
				done[op] = True
				remove.update(instrs)
		if not remove:
			break
		for instrs in op2instr:
			if len(instrs) != 1:
				instrs.difference_update(remove)

	done = False
	for op, instrs in enumerate(op2instr):
		print(op, '=>', ', '.join([instruction_names[i] for i in instrs]))
		if len(instrs) != 1:
			print('More than one instruction for opcode', op)
			done = True
	if done:
		return None

	return [instructions[instrs.pop()] for instrs in op2instr]

def read_input():
	register_pattern_str = '\\[([0123]), ([0123]), ([0123]), ([0123])\\]$'
	before_pattern = re.compile('^Before: ' + register_pattern_str)
	after_pattern = re.compile('^After:  ' + register_pattern_str)
	instr_pattern = re.compile('^([0123456789]|1[012345]) ([0123]) ([0123]) ([0123])$')

	patterns = (before_pattern, instr_pattern, after_pattern, None)
	pattern_index = 0
	sample = []
	samples = []
	program = []
	line_number = 0

	for line in sys.stdin:
		line_number += 1
		pattern = patterns[pattern_index]
		if pattern:
			m = pattern.match(line)
			if not m:
				break
			sample.append(list(map(int, m.groups())))
			pattern_index += 1
		elif line != '\n':
			break
		else:
			samples.append(sample)
			pattern_index = 0
			sample = []

	if pattern_index != 0 or line != '\n':
		print('Line', line_number, 'doesn\'t match expected pattern!')
		return None, None

	for line in sys.stdin:
		line_number += 1
		m = instr_pattern.match(line)
		if m:
			program.append(list(map(int, m.groups())))
		elif line != '\n':
			print('Line', line_number, 'doesn\'t match expected pattern!')
			return None, None

	return samples, program

def main():
	samples, program = read_input()
	if not samples:
		return

	op2instr = make_op2instr(samples)
	if not op2instr:
		return

	registers = [0] * 4
	print(registers)
	for op, a, b, c in program:
		registers[c] = op2instr[op](registers, a, b)
	print(registers)

if __name__ == '__main__':
	main()

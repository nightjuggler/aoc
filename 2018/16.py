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

def try_instr(before, instr, after):
	op, a, b, c = instr
	before_value = before[c]
	after_value = after[c]
	before[c] = after_value
	if before != after:
		return 0
	before[c] = before_value
	possible = 0
	for instr in instructions:
		if instr(before, a, b) == after_value:
			possible += 1
	return possible

def main():
	register_pattern_str = '\\[([0123]), ([0123]), ([0123]), ([0123])\\]$'
	before_pattern = re.compile('^Before: ' + register_pattern_str)
	after_pattern = re.compile('^After:  ' + register_pattern_str)
	instr_pattern = re.compile('^([0123456789]|1[012345]) ([0123]) ([0123]) ([0123])$')

	patterns = (before_pattern, instr_pattern, after_pattern, None)
	pattern_index = 0
	args = []

	line_number = 0
	three_or_more = 0

	for line in sys.stdin:
		line_number += 1
		pattern = patterns[pattern_index]
		if pattern:
			m = pattern.match(line)
			if not m:
				break
			args.append(list(map(int, m.groups())))
			pattern_index += 1
		elif line != '\n':
			break
		else:
			if try_instr(*args) > 2:
				three_or_more += 1
			pattern_index = 0
			args = []

	if pattern_index != 0 or line != '\n':
		print('Line', line_number, 'doesn\'t match expected pattern!')
		return

	print(three_or_more)

if __name__ == '__main__':
	main()

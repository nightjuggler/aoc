from collections import defaultdict
import operator
import re
import sys

def main():
	r = '([a-z]+)'
	n = '(-?[1-9][0-9]*|0)'
	pattern = re.compile(f'{r} (inc|dec) {n} if {r} (<=?|>=?|==|!=) {n}$')
	regs = defaultdict(int)
	ops = {
		'<':  operator.lt,
		'<=': operator.le,
		'==': operator.eq,
		'!=': operator.ne,
		'>=': operator.ge,
		'>':  operator.gt,
	}
	max_value = 0
	for line_num, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		r1, op1, n1, r2, op2, n2 = m.groups()
		if ops[op2](regs[r2], int(n2)):
			v = regs[r1]
			if op1 == 'inc':
				v += int(n1)
			else:
				v -= int(n1)
			regs[r1] = v
			if v > max_value:
				max_value = v
	print('Part 1:', max(regs.values()))
	print('Part 2:', max_value)

main()

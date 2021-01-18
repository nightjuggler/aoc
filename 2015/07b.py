import re
import sys

def main(input_file):
	line_number = 0
	line_pattern = re.compile('^({x}|(?:{x} (?:AND|OR|[LR]SHIFT) {x})'
		'|(?:NOT {x})) -> ([a-z]+)$'.format(x='(?:0|[1-9][0-9]*|[a-z]+)'))

	wires = {}

	def value(x):
		if x[0] in '0123456789':
			return int(x)
		n = wires[x]
		if isinstance(n, int):
			return n
		func, args = n
		wires[x] = n = func(*args) % (1 << 16)
		return n

	f_value = lambda x: value(x)
	f_not = lambda x: ~value(x)
	f_and = lambda a, b: value(a) & value(b)
	f_or = lambda a, b: value(a) | value(b)
	f_lshift = lambda a, b: value(a) << value(b)
	f_rshift = lambda a, b: value(a) >> value(b)

	for line in input_file:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
		src, dst = m.groups()
		src = src.split()
		srclen = len(src)
		if srclen == 1:
			func = f_value
			args = (src[0],)
		elif srclen == 2:
			assert src[0] == 'NOT'
			func = f_not
			args = (src[1],)
		else:
			assert srclen == 3
			src1, op, src2 = src
			args = (src1, src2)
			if   op == 'AND': func = f_and
			elif op == 'OR':  func = f_or
			elif op == 'LSHIFT': func = f_lshift
			elif op == 'RSHIFT': func = f_rshift
			else:
				assert False
		wires[dst] = (func, args)

	wires2 = wires.copy()
	wires2['b'] = value('a')
	wires = wires2
	print(value('a'))

if __name__ == '__main__':
	main(sys.stdin)

import re
import sys

def main(data):
	n = '([1-9][0-9]{0,2}|0)'
	pattern = re.compile(f'mul\\({n},{n}\\)|do\\(\\)|don\'t\\(\\)')
	enabled = True
	sum1 = sum2 = 0
	for m in pattern.finditer(data):
		s = m.group(0)
		if s == 'do()':
			enabled = True
		elif s == 'don\'t()':
			enabled = False
		else:
			a, b = map(int, m.groups())
			sum1 += a * b
			if enabled:
				sum2 += a * b
	print('Part 1:', sum1)
	print('Part 2:', sum2)

if __name__ == '__main__':
	main(sys.stdin.read())

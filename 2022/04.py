import re
import sys

def main():
	n = '([1-9][0-9]*)'
	pattern = re.compile(f'^{n}-{n},{n}-{n}$')
	contains = 0
	overlaps = 0
	for line_num, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f'Line {line_num} doesn\'t match pattern!')
		a1, a2, b1, b2 = map(int, m.groups())
		assert a1 <= a2
		assert b1 <= b2
		if a1 >= b1 and a2 <= b2 or b1 >= a1 and b2 <= a2:
			contains += 1
		if b1 <= a1 <= b2 or a1 <= b1 <= a2:
			overlaps += 1
	print('Part 1:', contains)
	print('Part 2:', overlaps)

main()

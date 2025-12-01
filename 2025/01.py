import re
import sys

def part1(rots):
	dial = 50
	return sum(1 for n in rots if not (dial := (dial + n) % 100))

def part2(rots):
	dial = 50
	password = 0
	flipped = False
	for n in rots:
		if (left := n < 0): n = -n
		if left != flipped:
			if dial: dial = 100 - dial
			flipped = left
		dial += n
		if dial > 99:
			password += dial // 100
			dial %= 100
	return password

def main(f):
	pattern = re.compile('^[LR][1-9][0-9]*$')
	rots = []
	for line_num, line in enumerate(f, start=1):
		if not pattern.match(line):
			return f'Line {line_num} doesn\'t match the expected pattern!'
		n = int(line[1:])
		if line[0] == 'L': n = -n
		rots.append(n)

	print('Part 1:', part1(rots))
	print('Part 2:', part2(rots))

if __name__ == '__main__':
	sys.exit(main(sys.stdin))

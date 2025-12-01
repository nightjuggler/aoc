import re
import sys

def main(f):
	dial = 50
	flipped = False
	part1 = part2 = 0
	pattern = re.compile('^[LR][1-9][0-9]*$')

	for line_num, line in enumerate(f, start=1):
		if not pattern.match(line):
			return f'Line {line_num} doesn\'t match the expected pattern!'
		left = line[0] == 'L'
		if flipped != left:
			if dial: dial = 100 - dial
			flipped = left
		dial += int(line[1:])
		if dial > 99:
			part2 += dial // 100
			dial %= 100
			if not dial: part1 += 1

	print('Part 1:', part1)
	print('Part 2:', part2)

if __name__ == '__main__':
	sys.exit(main(sys.stdin))

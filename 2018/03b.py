import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def overlap(fabric, x1, y1, x2, y2):
	for y in range(y1, y2):
		for x in range(x1, x2):
			if fabric[y][x] > 1:
				return True
	return False

def main():
	claims = []
	max_x = max_y = 0
	line_pattern = re.compile('^#({n}) @ ({n}|0),({n}|0): ({n})x({n})$'.format(n='[1-9][0-9]*'))

	for i, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', i)
		n, x, y, w, h = map(int, m.groups())
		x2 = x + w
		y2 = y + h
		if x2 > max_x: max_x = x2
		if y2 > max_y: max_y = y2
		claims.append((n, x, y, x2, y2))

	print(max_y, 'x', max_x)
	fabric = [[0] * max_x for i in range(max_y)]

	for n, x1, y1, x2, y2 in claims:
		for y in range(y1, y2):
			for x in range(x1, x2):
				fabric[y][x] += 1

	for n, x1, y1, x2, y2 in claims:
		if not overlap(fabric, x1, y1, x2, y2):
			print(n)

if __name__ == '__main__':
	main()

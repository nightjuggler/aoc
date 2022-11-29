import sys

def get_distance(x, y):
	if x < 0 and y > 0:
		d = min(-x, y)
		return d + abs(x + d) + abs(y - d)
	if x > 0 and y < 0:
		d = min(x, -y)
		return d + abs(x - d) + abs(y + d)
	return abs(x) + abs(y)

def main(path):
	x = y = 0
	distance = furthest = 0

	for d in path.split(','):
		if   d == 'se': y += 1
		elif d == 'nw': y -= 1
		elif d == 'ne': x += 1
		elif d == 'sw': x -= 1
		elif d == 'n':
			x += 1
			y -= 1
		elif d == 's':
			x -= 1
			y += 1
		else:
			sys.exit('Unexpected direction!')
		distance = get_distance(x, y)
		if distance > furthest:
			furthest = distance

	print('Part 1:', distance)
	print('Part 2:', furthest)

main(sys.stdin.readline().strip())

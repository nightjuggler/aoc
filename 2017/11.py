import sys

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
		distance = abs(x) + abs(y)
		if x*y < 0:
			distance -= min(abs(x), abs(y))
		if distance > furthest:
			furthest = distance

	print('Part 1:', distance)
	print('Part 2:', furthest)

main(sys.stdin.readline().strip())

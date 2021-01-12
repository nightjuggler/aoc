import sys

class ParseError(Exception):
	def __init__(self, column, message):
		self.column = column
		self.message = message

def err(column, message):
	raise ParseError(column, message)

def parse(line):
	x = 0
	y = 0
	n = len(line)
	i = 0
	while i != n:
		if line[i] == 'e':
			x += 1
		elif line[i] == 'w':
			x -= 1
		elif line[i] == 'n':
			i += 1
			if i == n:
				err(i, 'Expected e or w following n!')
			y += 1
			if line[i] == 'w':
				x -= 1
			elif line[i] != 'e':
				err(i, 'Expected e or w following n!')
		elif line[i] == 's':
			i += 1
			if i == n:
				err(i, 'Expected e or w following s!')
			y -= 1
			if line[i] == 'e':
				x += 1
			elif line[i] != 'w':
				err(i, 'Expected e or w following s!')
		elif line[i] == '\n':
			if i + 1 != n:
				err(i, 'Newline not at end of line?!')
			break
		else:
			err(i, 'Expected e, n, s, or w!')
		i += 1
	return (x, y)

def neighbors(x, y):
	return ((x+1,y), (x-1,y), (x-1,y+1), (x,y+1), (x,y-1), (x+1,y-1))

def play(tiles):
	black = set()
	white = set()

	for xy in tiles:
		n = 0
		for a in neighbors(*xy):
			if a in tiles:
				n += 1
			elif a not in white:
				an = 0
				for b in neighbors(*a):
					if b in tiles:
						an += 1
				if an == 2:
					black.add(a)
				white.add(a)
		if n == 1 or n == 2:
			black.add(xy)

	return black

def main(f):
	tiles = {}
	for line_number, line in enumerate(f, start=1):
		try:
			xy = parse(line)
		except ParseError as e:
			print('Line {}, column {}:'.format(line_number, e.column), e.message, file=sys.stderr)
			continue
		tiles[xy] = not tiles.get(xy, False)

	tiles = set([xy for xy, black in tiles.items() if black])

	for day in range(1, 101):
		tiles = play(tiles)
		print('Day {}: {}'.format(day, len(tiles)))

if __name__ == '__main__':
	main(sys.stdin)

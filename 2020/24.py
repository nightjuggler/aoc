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

def main(f):
	tiles = {}
	for line_number, line in enumerate(f, start=1):
		try:
			xy = parse(line)
		except ParseError as e:
			print('Line {}, column {}:'.format(line_number, e.column), e.message, file=sys.stderr)
			continue
		tiles[xy] = not tiles.get(xy, False)

#	for xy, black in tiles.items():
#		print(xy, '=>', 'Black' if black else 'White')

	num_black = 0
	for black in tiles.values():
		if black:
			num_black += 1
	print(num_black)

if __name__ == '__main__':
	main(sys.stdin)

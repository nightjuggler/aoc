import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

class Cart(object):
	def __init__(self, x, y, dx, dy):
		self.yx = (y, x)
		self.dxdy = (dx, dy)
		self.turn = 0

def read_input(f):
	grid = []
	carts = []
	for y, line in enumerate(f):
		row = []
		for x, c in enumerate(line):
			if c == '<':
				c = '-'
				carts.append(Cart(x, y, -1, 0))
			elif c == '>':
				c = '-'
				carts.append(Cart(x, y, 1, 0))
			elif c == '^':
				c = '|'
				carts.append(Cart(x, y, 0, -1))
			elif c == 'v':
				c = '|'
				carts.append(Cart(x, y, 0, 1))
			elif c not in ' +-/\\|\n':
				err('Unexpected character at row {}, column {}!', y, x)
			row.append(c)
		grid.append(''.join(row))
	return grid, carts

def main():
	grid, carts = read_input(sys.stdin)
	cart_locations = set([c.yx for c in carts])
	num_carts = len(carts)

	while num_carts > 1:
		carts.sort(key=lambda c: c.yx)
		i = 0
		while i < num_carts:
			c = carts[i]
			cart_locations.remove(c.yx)
			y, x = c.yx
			dx, dy = c.dxdy
			x += dx
			y += dy
			c.yx = yx = (y, x)
			if yx in cart_locations:
				print('Crash at {},{}'.format(x, y))
				cart_locations.remove(yx)
				del carts[i]
				for j, c in enumerate(carts):
					if yx == c.yx:
						break
				del carts[j]
				num_carts -= 2
				if j < i:
					i -= 1
				continue
			cart_locations.add(yx)

			g = grid[y][x]
			if g == '-':
				assert dy == 0
			elif g == '|':
				assert dx == 0
			elif g == '/':
				c.dxdy = (0, -dx) if dy == 0 else (-dy, 0)
			elif g == '\\':
				c.dxdy = (0, dx) if dy == 0 else (dy, 0)
			elif g == '+':
				# 0 => left, 1 => straight, 2 => right
				if c.turn == 0:
					c.dxdy = (0, -dx) if dy == 0 else (dy, 0)
				elif c.turn == 2:
					c.dxdy = (0, dx) if dy == 0 else (-dy, 0)
				c.turn = (c.turn + 1) % 3
			else:
				err('Wtf? Cart derailed at {},{}!', x, y)
			i += 1

	if num_carts == 1:
		y, x = carts[0].yx
		print('One cart remaining at {},{}'.format(x, y))
	else:
		print('No carts remaining!')

if __name__ == '__main__':
	main()

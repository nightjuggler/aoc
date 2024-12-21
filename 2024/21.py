import sys

numpad = {key: (x, y)
	for y, row in enumerate(('789', '456', '123', '_0A'))
	for x, key in enumerate(row) if key != '_'}
dirpad = {key: (x, y)
	for y, row in enumerate(('_^A', '<v>'))
	for x, key in enumerate(row) if key != '_'}

def numpad_moves(keys):
	moves = []
	x1, y1 = numpad['A']
	for key in keys:
		x2, y2 = numpad[key]
		dx, dy = x2-x1, y2-y1
		if not x1 and y2 == 3:
			moves.append('>'*dx)
			moves.append('v'*dy)
		elif not x2 and y1 == 3:
			moves.append('^'*(-dy))
			moves.append('<'*(-dx))
		else:
			if dx < 0: moves.append('<'*(-dx))
			if dy > 0: moves.append('v'*dy)
			if dy < 0: moves.append('^'*(-dy))
			if dx > 0: moves.append('>'*dx)
		moves.append('A')
		x1, y1 = x2, y2
	return ''.join(moves)

def dirpad_lookup():
	lookup = {}
	for key1, (x1, y1) in dirpad.items():
		for key2, (x2, y2) in dirpad.items():
			moves = []
			dx, dy = x2-x1, y2-y1
			if not x1 and not y2:
				moves.append('>'*dx)
				moves.append('^'*(-dy))
			elif not x2 and not y1:
				moves.append('v'*dy)
				moves.append('<'*(-dx))
			else:
				if dx < 0: moves.append('<'*(-dx))
				if dy > 0: moves.append('v'*dy)
				if dy < 0: moves.append('^'*(-dy))
				if dx > 0: moves.append('>'*dx)
			moves.append('A')
			lookup[key1, key2] = ''.join(moves)
	return lookup

def main():
	cache = {}
	lookup = dirpad_lookup()

	def dirpad_moves(keys, depth):
		if not depth:
			return len(keys)
		if (keys, depth) in cache:
			return cache[keys, depth]
		n = 0
		key1 = 'A'
		for key2 in keys:
			n += dirpad_moves(lookup[key1, key2], depth-1)
			key1 = key2
		cache[keys, depth] = n
		return n

	sum1 = sum2 = 0
	for line in sys.stdin:
		assert line.endswith('A\n')
		code = int(line[:-2])
		keys = numpad_moves(line[:-1])
		n1 = dirpad_moves(keys, 2)
		n2 = dirpad_moves(keys, 25)
		sum1 += code * n1
		sum2 += code * n2
	print('Part 1:', sum1)
	print('Part 2:', sum2)
main()

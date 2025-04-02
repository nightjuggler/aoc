import sys

def make_lookup(*rows):
	keypad = {key: (x, y)
		for y, row in enumerate(rows)
		for x, key in enumerate(row)}
	gap = keypad.pop('_')
	lookup = {}
	for key1, (x1, y1) in keypad.items():
		for key2, (x2, y2) in keypad.items():
			moves = []
			dx, dy = x2-x1, y2-y1
			if (x1, y2) == gap:
				moves.append('>'*dx if dx > 0 else '<'*(-dx))
				moves.append('v'*dy if dy > 0 else '^'*(-dy))
			elif (x2, y1) == gap:
				moves.append('v'*dy if dy > 0 else '^'*(-dy))
				moves.append('>'*dx if dx > 0 else '<'*(-dx))
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
	numpad = make_lookup('789', '456', '123', '_0A')
	dirpad = make_lookup('_^A', '<v>')

	def numpad_moves(code):
		key1 = 'A'
		return ''.join([numpad[key1, key1 := key2] for key2 in code])

	def dirpad_moves(keys, depth):
		if not depth:
			return len(keys)
		if (keys, depth) in cache:
			return cache[keys, depth]
		key1 = 'A'
		cache[keys, depth] = n = sum(
			dirpad_moves(dirpad[key1, key1 := key2], depth-1) for key2 in keys)
		return n

	sum1 = sum2 = 0
	for line in sys.stdin:
		assert line.endswith('A\n')
		code = int(line[:-2])
		keys = numpad_moves(line[:-1])
		sum1 += code * dirpad_moves(keys, 2)
		sum2 += code * dirpad_moves(keys, 25)

	print('Part 1:', sum1)
	print('Part 2:', sum2)
main()

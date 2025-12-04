import sys

def solve_v1(rows): # ~400ms
	rolls = set((x,y) for y, row in enumerate(rows) for x, c in enumerate(row) if c == '@')

	def removable(xy):
		x, y = xy
		x1, x2, y1, y2 = x-1, x+1, y-1, y+1
		neighbors = {(x1,y1),(x,y1),(x2,y1),(x1,y),(x2,y),(x1,y2),(x,y2),(x2,y2)}
		return len(rolls & neighbors) < 4

	print('Part 1:', sum(map(removable, rolls)))

	num_rolls = len(rolls)
	while discard := set(filter(removable, rolls)): rolls -= discard
	print('Part 2:', num_rolls - len(rolls))

def solve_v2(rows): # ~350ms
	size = len(rows) + 2
	offsets = -size-1, -size, -size+1, -1, 1, size-1, size, size+1
	rolls = set(y*size + x
		for y, row in enumerate(rows, start=1)
		for x, c in enumerate(row, start=1) if c == '@')

	def removable(pos): return len(rolls & {pos+d for d in offsets}) < 4

	print('Part 1:', sum(map(removable, rolls)))

	num_rolls = len(rolls)
	while discard := set(filter(removable, rolls)): rolls -= discard
	print('Part 2:', num_rolls - len(rolls))

def solve_v3(rows): # ~90ms
	size = len(rows) + 2
	offsets = -size-1, -size, -size+1, -1, 1, size-1, size, size+1
	rolls = set(y*size + x
		for y, row in enumerate(rows, start=1)
		for x, c in enumerate(row, start=1) if c == '@')

	num_rolls = len(rolls)
	check = rolls
	while True:
		discard = set()
		touched = set()
		for pos in check:
			neighbors = rolls & {pos+d for d in offsets}
			if len(neighbors) < 4:
				discard.add(pos)
				touched.update(neighbors)
		if check is rolls:
			print('Part 1:', len(discard))
		if not discard: break
		rolls -= discard
		check = touched - discard
	print('Part 2:', num_rolls - len(rolls))

def main():
	rows = [row.strip() for row in sys.stdin]
	size = len(rows)
	assert all(len(row) == size for row in rows)
	solve_v3(rows)

if __name__ == '__main__':
	main()

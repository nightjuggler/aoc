import sys
def main():
	rows = [row.strip() for row in sys.stdin]
	size = len(rows)
	assert all(len(row) == size for row in rows)

	size += 2
	offsets = -size-1, -size, -size+1, -1, 1, size-1, size, size+1
	rolls = {y*size + x
			for y, row in enumerate(rows, start=1)
			for x, tile in enumerate(row, start=1) if tile == '@'}
	rolls = {pos: {pos + d for d in offsets} & rolls for pos in rolls}
	discard = [(pos, adj) for pos, adj in rolls.items() if len(adj) < 4]
	print('Part 1:', len(discard))

	num_rolls = len(rolls)
	while discard:
		todo = []
		for pos, adj in discard:
			del rolls[pos]
			for pos2 in adj:
				adj2 = rolls[pos2]
				adj2.remove(pos)
				if len(adj2) == 3:
					todo.append((pos2, adj2))
		discard = todo
	print('Part 2:', num_rolls - len(rolls))
main()

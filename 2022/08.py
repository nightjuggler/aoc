import sys
def main():
	rows = [list(map(int, line.strip())) for line in sys.stdin]
	cols = list(zip(*rows))
	num_visible = 0
	max_score = 0
	for y, row in enumerate(rows):
		for x, (tree, col) in enumerate(zip(row, cols)):
			is_visible = False
			score = 1
			for trees in (row[x::-1], row[x:], col[y::-1], col[y:]):
				distance = 0
				for height in trees[1:]:
					distance += 1
					if height >= tree: break
				else:
					is_visible = True
				score *= distance
			if is_visible:
				num_visible += 1
			if score > max_score:
				max_score = score
	print('Part 1:', num_visible)
	print('Part 2:', max_score)
main()

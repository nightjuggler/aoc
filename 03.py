import sys

def main():
	rows = []
	for row in sys.stdin:
		row = row.strip()
		if not row:
			sys.exit('Row {} is empty!'.format(len(rows) + 1))
		for c in row:
			if c != '.' and c != '#':
				sys.exit('Row {} doesn\'t match pattern!'.format(len(rows) + 1))
		rows.append(row)

	x, y = 0, 0
	dx, dy = 3, 1
	max_y = len(rows) - 1
	num_trees = 0

	while True:
		y += dy
		if y > max_y:
			break
		x += dx
		row = rows[y]
		if row[x % len(row)] == '#':
			num_trees += 1

	print(num_trees, 'trees')

if __name__ == '__main__':
	main()

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

	max_y = len(rows) - 1

	product = 1
	for dx, dy in ((1,1), (3,1), (5,1), (7,1), (1,2)):
		x, y = 0, 0
		num_trees = 0

		while True:
			y += dy
			if y > max_y: break
			x += dx
			row = rows[y]
			if row[x % len(row)] == '#':
				num_trees += 1

		print(num_trees, 'trees')
		product *= num_trees

	print('The product is', product)

if __name__ == '__main__':
	main()

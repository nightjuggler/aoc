import sys

def err(message, *args):
	sys.exit(message.format(*args))

def read_input():
	rows = []
	for y, row in enumerate(sys.stdin):
		rowlen = len(row) - 1
		if rowlen < 0 or row[rowlen] != '\n':
			err('Row {} doesn\'t end in a newline!', y+1)
		if rowlen == 0:
			err('Row {} is empty!', y+1)
		cols = []
		for c in row[:rowlen]:
			if c == 'L':
				cols.append(0)
			elif c == '.':
				cols.append(2)
			else:
				err('Row {} contains characters other than "L" and "."!', y+1)
		if rows and len(rows[0]) != rowlen:
			err('The length of row {} is different from previous rows!', y+1)
		rows.append(cols)
	return rows

def print_rows(rows):
	for cols in rows:
		print(''.join(['L' if c == 0 else '#' if c == 1 else '.' for c in cols]))

def count_occupied(rows):
	n = 0
	for cols in rows:
		for c in cols:
			if c == 1:
				n += 1
	return n

def occupied(rows, max_x, max_y, x, y):
	n = 0
	for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
		nx = x
		ny = y
		while True:
			nx += dx
			ny += dy
			if nx < 0 or nx > max_x or ny < 0 or ny > max_y:
				break
			seat = rows[ny][nx]
			if seat == 1:
				n += 1
				break
			elif seat == 0:
				break
	return n

def play(rows):
	new_rows = []
	changed = False
	max_y = len(rows) - 1

	for y, cols in enumerate(rows):

		new_cols = []
		new_rows.append(new_cols)
		max_x = len(cols) - 1

		for x, seat in enumerate(cols):
			if seat == 2: # floor
				new_cols.append(seat)
				continue
			n = occupied(rows, max_x, max_y, x, y)
			if seat == 0: # empty
				if n == 0:
					seat = 1
					changed = True
			elif n > 4:
				seat = 0
				changed = True
			new_cols.append(seat)

	rows[:] = new_rows
	return changed

def main():
	rows = read_input()
	while play(rows):
		pass
	print_rows(rows)
	print(count_occupied(rows), 'occupied seats')

if __name__ == '__main__':
	main()

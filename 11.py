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

def play(rows):
	new_rows = []
	changed = False
	max_y = len(rows) - 1

	for y, cols in enumerate(rows):

		new_cols = []
		new_rows.append(new_cols)
		first_row = y == 0
		last_row = y == max_y
		max_x = len(cols) - 1

		for x, seat in enumerate(cols):
			if seat == 2: # floor
				new_cols.append(seat)
				continue
			first_col = x == 0
			last_col = x == max_x
			n = 0 # number of neighbors
			if not first_row:
				prev_row = rows[y-1]
				if prev_row[x] == 1:
					n += 1
				if not first_col and prev_row[x-1] == 1:
					n += 1
				if not last_col and prev_row[x+1] == 1:
					n += 1
			if not first_col and cols[x-1] == 1:
				n += 1
			if not last_col and cols[x+1] == 1:
				n += 1
			if not last_row:
				next_row = rows[y+1]
				if next_row[x] == 1:
					n += 1
				if not first_col and next_row[x-1] == 1:
					n += 1
				if not last_col and next_row[x+1] == 1:
					n += 1
			if seat == 0: # empty
				if n == 0:
					seat = 1
					changed = True
			elif n >= 4:
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

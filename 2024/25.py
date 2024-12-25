import sys

def read_input(f):
	keys = []
	locks = []
	for item in f.read().split('\n\n'):
		item = item.split()
		assert len(item) == 7 and all(len(row) == 5 and row.strip('#.') == '' for row in item)
		item = [[tile == '#' for tile in row] for row in item]
		cols = list(map(sum, zip(*item)))
		if sum(item[0]) == 0:
			assert sum(item[6]) == 5
			keys.append(cols)
		else:
			assert sum(item[0]) == 5 and sum(item[6]) == 0
			locks.append(cols)
	return keys, locks

def main():
	keys, locks = read_input(sys.stdin)
	print(sum(1 for lock in locks for key in keys
		if all(lock_col + key_col <= 7 for lock_col, key_col in zip(lock, key))))

main()

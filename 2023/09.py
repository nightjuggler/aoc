import sys

def diffs(values):
	return [values[i] - values[i-1] for i in range(1, len(values))]

def next_value(values):
	return values[-1] + next_value(diffs(values)) if any(values) else 0

def prev_value(values):
	return values[0] - prev_value(diffs(values)) if any(values) else 0

def main():
	data = [list(map(int, line.split())) for line in sys.stdin]
	print('Part 1:', sum(map(next_value, data)))
	print('Part 2:', sum(map(prev_value, data)))
main()

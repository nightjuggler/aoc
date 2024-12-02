import sys

def is_safe(levels):
	if levels[0] > levels[1]:
		levels = levels[::-1]
	return all(0 < levels[i] - levels[i-1] < 4 for i in range(1, len(levels)))

def is_safe2(levels):
	return any(is_safe(levels[:i] + levels[i+1:]) for i in range(len(levels)))

def main():
	safe = safe2 = 0
	for line in sys.stdin:
		levels = list(map(int, line.split()))
		if is_safe(levels):
			safe += 1
		elif is_safe2(levels):
			safe2 += 1

	print('Part 1:', safe)
	print('Part 2:', safe + safe2)

if __name__ == '__main__':
	main()

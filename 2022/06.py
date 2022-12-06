import sys

def marker(s, n):
	for i in range(n, len(s)+1):
		if len(set(s[i-n:i])) == n:
			return i
	return None

def main():
	s = sys.stdin.readline().strip()
	print('Part 1:', marker(s, 4))
	print('Part 2:', marker(s, 14))

main()

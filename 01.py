import sys

def main():
	s = set()
	for line in sys.stdin:
		n = int(line.strip())
		m = 2020 - n
		if m in s:
			print('{} * {} = {}'.format(m, n, m * n))
			break
		s.add(n)

if __name__ == '__main__':
	main()

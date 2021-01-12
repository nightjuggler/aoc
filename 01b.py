import sys

def main():
	s1 = set()
	s2 = {}
	for line in sys.stdin:
		n = int(line.strip())
		m = 2020 - n
		if n in s2:
			n1 = s2[n]
			n2 = m - n1
			print('{} * {} * {} = {}'.format(n1, n2, n, n1*n2*n))
			break
		for n1 in s1:
			n2 = m - n1
			if n2 > 0:
				s2[n2] = n1
		s1.add(n)

if __name__ == '__main__':
	main()

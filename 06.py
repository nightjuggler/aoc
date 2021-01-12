import sys

def main():
	s = set()
	answer = 0
	line_number = 0
	for line in sys.stdin:
		line_number += 1
		line = line.strip()
		if line:
			for c in line:
				if not (97 <= ord(c) <= 122):
					sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
				s.add(c)
		else:
			answer += len(s)
			s.clear()
	answer += len(s)
	print(answer)

if __name__ == '__main__':
	main()

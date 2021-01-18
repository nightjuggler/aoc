import sys

def main():
	group = None
	answer = 0
	line_number = 0
	for line in sys.stdin:
		line_number += 1
		line = line.strip()
		if line:
			person = set()
			for c in line:
				if not (97 <= ord(c) <= 122):
					sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
				person.add(c)
			if group is None:
				group = person
			else:
				group &= person
		else:
			if group:
				answer += len(group)
			group = None
	if group:
		answer += len(group)
	print(answer)

if __name__ == '__main__':
	main()

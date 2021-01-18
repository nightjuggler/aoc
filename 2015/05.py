import re
import sys

def main(input_file):
	line_pattern = re.compile('^[a-z]+$')
	disallowed_pairs = set([tuple([c for c in s]) for s in ('ab', 'cd', 'pq', 'xy')])
	nice = 0
	for line_number, line in enumerate(input_file):
		if not line_pattern.match(line):
			sys.exit('Line {} doesn\'t match pattern!'.format(line_number))
		vowel = 0
		prev = None
		double_letter = False
		disallowed = False
		for c in line:
			if c in 'aeiou':
				vowel += 1
			if c == prev:
				double_letter = True
			if (prev, c) in disallowed_pairs:
				disallowed = True
			prev = c
		if vowel >= 3 and double_letter and not disallowed:
			nice += 1
	print(nice)

if __name__ == '__main__':
	main(sys.stdin)

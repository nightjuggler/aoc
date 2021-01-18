import sys

def main(input_file):
	nice = 0
	for line in input_file:
		pair = repeat = False
		pairs = {}
		p = q = None
		for i, c in enumerate(line):
			if not pair:
				pc = (p, c)
				pair_index = pairs.get(pc)
				if pair_index is None:
					pairs[pc] = i
				elif i > pair_index + 1:
					pair = True
			if c == q:
				repeat = True
			q = p
			p = c
		if pair and repeat:
			nice += 1
	print(nice)

if __name__ == '__main__':
	main(sys.stdin)

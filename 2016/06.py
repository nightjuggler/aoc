from collections import Counter
import sys

def main():
	lines = [line.rstrip() for line in sys.stdin]
	print('Part 1:', ''.join([Counter(column).most_common(1)[0][0] for column in zip(*lines)]))
	print('Part 2:', ''.join([Counter(column).most_common()[-1][0] for column in zip(*lines)]))

main()

import sys

def read_input():
	patterns = []
	pattern = None
	for line in sys.stdin:
		line = line.rstrip()
		if not line:
			pattern = None
			continue
		if not pattern:
			patterns.append(pattern := [])
		pattern.append(line)
	return patterns

def find_reflection(pattern, old_r=0):
	n = len(pattern)
	for r in range(1, n):
		if all(pattern[r-i-1] == pattern[r+i] for i in range(min(r, n-r))) and r != old_r:
			return r
	return 0

def part1(pattern):
	return find_reflection(pattern)*100 or find_reflection(list(zip(*pattern)))

def part2(pattern_num, pattern, score):
	horz, vert = divmod(score, 100)
	for y in range(len(pattern)):
		row = pattern[y]
		for x, c in enumerate(row):
			pattern[y] = '.#'[c == '.'].join((row[:x], row[x+1:]))
			score = find_reflection(pattern, horz)*100 or find_reflection(list(zip(*pattern)), vert)
			if score:
				return score
		pattern[y] = row
	print(f'No different line of reflection for pattern {pattern_num}!')
	return 0

def main():
	patterns = read_input()
	print('Part 1:', sum(scores := list(map(part1, patterns))))
	print('Part 2:', sum(map(part2, range(len(patterns)), patterns, scores)))
main()

import re
import sys

def read_input(f):
	template = f.readline().rstrip()
	if not template:
		print('Please specify the polymer template on input line 1!')
		return None, None

	rules = {}
	rule_pattern = re.compile('^([A-Z]{2}) -> ([A-Z])$')

	for line_number, line in enumerate(f, start=2):
		if m := rule_pattern.match(line):
			pair, c = m.groups()
			rules[pair] = c
		elif line.rstrip():
			print(f'Please specify a valid rule on input line {line_number}!')
			return None, None

	return template, rules

def solve(template, rules, steps):
	pairs = {}
	for i in range(len(template) - 1):
		pair = template[i:i+2]
		pairs[pair] = pairs.get(pair, 0) + 1

	freq = {}
	for c in template:
		freq[c] = freq.get(c, 0) + 1

	for step in range(steps):
		new_pairs = {}
		for pair, n in pairs.items():
			c = rules.get(pair)
			if c:
				p = pair[0] + c
				new_pairs[p] = new_pairs.get(p, 0) + n
				p = c + pair[1]
				new_pairs[p] = new_pairs.get(p, 0) + n
				freq[c] = freq.get(c, 0) + n
			else:
				new_pairs[pair] = new_pairs.get(pair, 0) + n
		pairs = new_pairs

	freq = list(freq.values())
	freq.sort()

	return freq[-1] - freq[0]

def main():
	template, rules = read_input(sys.stdin)
	if template:
		print('Part 1 (10 steps):', solve(template, rules, 10))
		print('Part 2 (40 steps):', solve(template, rules, 40))

if __name__ == '__main__':
	main()

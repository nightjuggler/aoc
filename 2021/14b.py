from collections import Counter
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
	pairs = Counter([template[i:i+2] for i in range(len(template) - 1)])
	freq = Counter(template)

	for step in range(steps):
		new_pairs = Counter()
		for pair, n in pairs.items():
			c = rules.get(pair)
			if c:
				new_pairs[pair[0] + c] += n
				new_pairs[c + pair[1]] += n
				freq[c] += n
			else:
				new_pairs[pair] += n
		pairs = new_pairs

	freq = freq.most_common()
	return freq[0][1] - freq[-1][1]

def main():
	template, rules = read_input(sys.stdin)
	if template:
		print('Part 1 (10 steps):', solve(template, rules, 10))
		print('Part 2 (40 steps):', solve(template, rules, 40))

if __name__ == '__main__':
	main()

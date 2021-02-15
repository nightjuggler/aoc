import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def read_input(f):
	state_pattern = re.compile('^initial state: [.#]+$')
	rule_pattern = re.compile('^[.#]{5} => [.#]$')

	line = f.readline().rstrip()
	if not state_pattern.match(line):
		err('Line 1 doesn\'t match pattern!')

	state = set([i for i, c in enumerate(line[15:]) if c == '#'])

	if f.readline().rstrip() != '':
		err('Line 2 doesn\'t match pattern!')

	rules = {}
	for i, line in enumerate(f, start=3):
		if not rule_pattern.match(line):
			err('Line {} doesn\'t match pattern!', i)
		rule = line[:5]
		if rule in rules:
			err('Line {}: Rule for "{}" already defined!', i, rule)
		if line[9] == '.':
			rules[rule] = False
			continue
		if rule == '.....':
			err('Line {}: Rule "{} => {}" not allowed!', i, rule, line[9])
		rules[rule] = True

	return state, set([rule for rule, alive in rules.items() if alive])

def main():
	state, rules = read_input(sys.stdin)

	f = lambda i: '#' if i in state else '.'
	alive = lambda i, c: ''.join([f(i-2), f(i-1), c, f(i+1), f(i+2)]) in rules

	for generation in range(20):
		done = {}
		for i in state:
			if alive(i, '#'):
				done[i] = True
			for j in (-2, -1, 1, 2):
				k = i + j
				if k in state or k in done:
					continue
				done[k] = alive(k, '.')

		state = set([i for i, alive in done.items() if alive])

	print(sum(state))

if __name__ == '__main__':
	main()

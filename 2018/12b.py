import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def read_input(f):
	state_pattern = re.compile('^initial state: #[.#]*#$')
	rule_pattern = re.compile('^[.#]{5} => [.#]$')

	line = f.readline().rstrip()
	if not state_pattern.match(line):
		err('Line 1 doesn\'t match pattern!')

	state = [i for i, c in enumerate(line[15:]) if c == '#']

	if f.readline().rstrip() != '':
		err('Line 2 doesn\'t match pattern!')

	rules = [None] * 32
	for i, line in enumerate(f, start=3):
		if not rule_pattern.match(line):
			err('Line {} doesn\'t match pattern!', i)
		rule = sum([(c == '#') << i for i, c in enumerate(line[:5])])
		if rules[rule] is not None:
			err('Line {}: Rule for "{}" already defined!', i, line[:5])
		if line[9] == '.':
			rules[rule] = False
			continue
		if rule == 0:
			err('Line {}: Rule "{} => {}" not allowed!', i, line[:5], line[9])
		rules[rule] = True

	return state, [bool(rule) for rule in rules]

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--generations', '-g', type=int, default=50_000_000_000)
	args = parser.parse_args()

	num_gen = args.generations
	if num_gen < 0:
		err('The number of generations must be >= 0!')

	state, rules = read_input(sys.stdin)

	offset = 0
	hi = state[-1]
	state = set(state)

	for gen in range(num_gen):
		new_state = []
		rule = 0
		for i in range(-2, hi + 3):
			rule += (i + 2 in state) << 4
			if rules[rule]:
				new_state.append(i)
			rule >>= 1
		if not new_state:
			err('There are no plants after {} generations!', gen + 1)
		lo = new_state[0]
		new_state = [i - lo for i in new_state]
		hi = new_state[-1]
		new_state = set(new_state)
		if state == new_state:
			print('No change after {} generations!'.format(gen + 1))
			offset += lo * (num_gen - gen)
			break
		state = new_state
		offset += lo

	print(sum(state) + offset * len(state))

if __name__ == '__main__':
	main()

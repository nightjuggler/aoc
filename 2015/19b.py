import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def read_rules(f):
	line_pattern = re.compile('^(?:[A-Z][a-z]?|e) => (?:[A-Z][a-z]?)+$')

	rules = {}
	e_rules = set()
	table = {i: None for i in range(ord('a'), ord('z') + 1)}

	for i, line in enumerate(f, start=1):
		line = line.rstrip()
		if not line_pattern.match(line):
			if not line:
				break
			err('Line {} doesn\'t match pattern!', i)

		a, b = line.split(' => ')
		blen = len(b.translate(table))
		if blen == 1:
			assert a == 'e'
		if a == 'e':
			assert b not in e_rules
			e_rules.add(b)
		else:
			assert b not in rules
			rules[b] = (blen, b, a)

	rules = [(b, a) for blen, b, a in sorted(rules.values(), reverse=True)]
	return rules, e_rules

def reduce_molecule(molecule, rules, e_rules, verbose=0):
	step = 0
	while molecule not in e_rules:
		for old, new in rules:
			new_molecule = molecule.replace(old, new, 1)
			if new_molecule != molecule:
				molecule = new_molecule
				step += 1
				if verbose:
					print(step, old, '=>', new)
					if verbose > 1:
						print(molecule)
				break
		else:
			print('Cannot be reduced to e!')
			return False
	step += 1
	if verbose:
		print(step, molecule, '=>', 'e')

	print('Reduced to e in', step, 'steps')
	return True

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('inputfile', nargs='?', default='data/19.input')
	parser.add_argument('-v', '--verbose', action='count')
	args = parser.parse_args()

	with open(args.inputfile) as f:
		rules, e_rules = read_rules(f)
		molecule = f.readline().rstrip()

	reduce_molecule(molecule, rules, e_rules, args.verbose)

if __name__ == '__main__':
	main()

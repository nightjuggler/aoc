import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def match(rules, n, s):
	if isinstance(n, tuple):
		subrule, subrule_index = n
		iset = match(rules, subrule[subrule_index], s)
		if not iset:
			return iset
		subrule_index += 1
		if subrule_index == len(subrule):
			return iset
		jset = set()
		for i in iset:
			for j in match(rules, (subrule, subrule_index), s[i:]):
				jset.add(i + j)
		return jset

	rule = rules[n]
	if isinstance(rule, str):
		return set([len(rule)]) if s.startswith(rule) else set()

	iset = set()
	for subrule in rule:
		iset.update(match(rules, (subrule, 0), s))
	return iset

def main():
	line_number = 0
	pattern1 = re.compile('^(0|[1-9][0-9]*): ')
	pattern2 = re.compile('^[1-9][0-9]*(?: [1-9][0-9]*)*(?: \\| [1-9][0-9]*(?: [1-9][0-9]*)*)*$')
	pattern3 = re.compile('^"[ab]"$')
	pattern4 = re.compile('^[ab]+$')
	rules = {}

	for line in sys.stdin:
		line_number += 1
		line = line.rstrip()
		if not line:
			break
		m = pattern1.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', line_number)
		rule_number = int(m.group(1))
		line = line[m.end():]
		m = pattern2.match(line)
		if m:
			rules[rule_number] = [[int(n) for n in subrule.split()]
				for subrule in line.split(' | ')]
			continue
		m = pattern3.match(line)
		if m:
			rules[rule_number] = line[1]
			continue
		err('Line {} doesn\'t match pattern!', line_number)

	rules[8] = [[42], [42, 8]]
	rules[11] = [[42, 31], [42, 11, 31]]

#	for rule_number, rule in sorted(rules.items()):
#		print(rule_number, '=>', rule)

	num_match = 0
	for line in sys.stdin:
		line_number += 1
		line = line.rstrip()
		m = pattern4.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', line_number)
		linelen = len(line)
		m = match(rules, 0, line)
#		print(line, linelen, m)
		if linelen in m:
			num_match += 1
	print(num_match)

if __name__ == '__main__':
	main()

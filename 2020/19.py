import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def match(rules, n, s):
	rule = rules[n]
	if isinstance(rule, str):
		return len(rule) if s.startswith(rule) else 0
	for subrule in rule:
		j = 0
		for n in subrule:
			i = match(rules, n, s[j:])
			if i == 0:
				break
			j += i
		else:
			return j
	return 0

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

#	for rule_number, rule in sorted(rules.items()):
#		print(rule_number, '=>', rule)

	num_match = 0
	for line in sys.stdin:
		line_number += 1
		line = line.rstrip()
		m = pattern4.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', line_number)
		if match(rules, 0, line) == len(line):
			num_match += 1
	print(num_match)

if __name__ == '__main__':
	main()

import re
import sys

def tokenize(s):
	max_i = len(s) - 1
	if max_i < 0:
		print('tokenize(): Expected non-empty string!')
		return []

	t = []
	i = 0
	a = ord(s[0])

	while True:
		if not (65 <= a <= 90):
			print('tokenize("{}"): Expected uppercase letter at position {}!'.format(s, i))
			break
		if i == max_i:
			t.append(chr(a))
			break
		i += 1
		b = ord(s[i])
		if 97 <= b <= 122:
			t.append(chr(a) + chr(b))
			if i == max_i:
				break
			i += 1
			a = ord(s[i])
		else:
			t.append(chr(a))
			a = b
	return t

def read_rules(f):
	line_pattern = re.compile('^[A-Z][a-z]? => (?:[A-Z][a-z]?)+$')

	rules = {}
	for line in f:
		line = line.rstrip()
		if not line_pattern.match(line):
			if not line:
				break
			print('Skipping "{}"'.format(line))
			continue
		a, b = line.split(' => ')
		r = rules.get(a)
		if r is None:
			rules[a] = r = []
		r.append(tokenize(b))
	return rules

def main(f):
	rules = read_rules(f)
	molecule = tokenize(f.readline().rstrip())
	molecules = set()

	for i in range(len(molecule)):
		e = molecule[i]
		r = rules.get(e)
		if r is None:
			continue
		for p in r:
			molecule[i:i+1] = p
			molecules.add(''.join(molecule))
			molecule[i:i+len(p)] = [e]

	print(len(molecules))

if __name__ == '__main__':
	main(sys.stdin)

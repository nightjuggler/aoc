import re
import sys

def maximize(names, happiness):
	max_h = 0
	max_i = len(names) - 1
	if max_i < 2:
		return 0

	def add_happiness():
		nonlocal max_h
		h = 0
		i = 0
		j = max_i
		for name in names:
			k = 0 if i == max_i else i + 1
			h += happiness[(name, names[j])] + happiness[(name, names[k])]
			j = i
			i = k
		if h > max_h:
			max_h = h
#		print('-'.join(names), '=', h)

	def recurse(i):
		if i == max_i:
			add_happiness()
			return
		recurse(i + 1)
		for j in range(i + 1, max_i + 1):
			names[i], names[j] = names[j], names[i]
			recurse(i + 1)
			names[i], names[j] = names[j], names[i]

	recurse(1)
	return max_h

def main(input_file):
	line_pattern = re.compile('^([A-Z][a-z]+) would (gain|lose) ([1-9][0-9]*) '
		'happiness units by sitting next to ([A-Z][a-z]+)\\.$')

	names = set()
	happiness = {}

	for line_number, line in enumerate(input_file):
		m = line_pattern.match(line)
		if not m:
			print('Line {} doesn\'t match pattern!'.format(line_number))
			return
		name1, gain_lose, units, name2 = m.groups()
		units = int(units)
		if gain_lose == 'lose':
			units = -units
		happiness[(name1, name2)] = units
		names.add(name1)

	print(maximize(list(names), happiness))

if __name__ == '__main__':
	main(sys.stdin)

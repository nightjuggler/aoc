import sys

def main(stream):
	stream = iter(stream)
	score = garbage = 0
	groups = [0]
	p = None
	for c in stream:
		if c == '{':
			assert p == '{' or p == ',' or p is None
			group = groups[-1] + 1
			groups.append(group)
			score += group
		elif c == '<':
			assert p == '{' or p == ','
			for c in stream:
				if c == '>': break
				if c == '!': next(stream)
				else:
					garbage += 1
		elif c == ',':
			assert p == '}' or p == '>'
		elif c == '}':
			assert p == '}' or p == '>' or p == '{'
			groups.pop()
		else:
			sys.exit('Unexpected character!')
		p = c
	assert groups == [0]
	print('Part 1:', score)
	print('Part 2:', garbage)

main(sys.stdin.readline().rstrip())

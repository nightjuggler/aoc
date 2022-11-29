import sys

def main(stream):
	stream = iter(stream)
	group = score = garbage = 0
	p = None
	for c in stream:
		if c == '{':
			assert p == '{' or p == ',' or p is None
			group += 1
			score += group
		elif c == '<':
			assert p == '{' or p == ','
			for c in stream:
				if c == '>': break
				if c == '!': next(stream)
				else:
					garbage += 1
		elif c == ',':
			assert (p == '}' and group) or p == '>'
		elif c == '}':
			assert (p == '}' and group) or p == '>' or p == '{'
			group -= 1
		else:
			sys.exit('Unexpected character!')
		p = c
	assert p == '}' and not group
	print('Part 1:', score)
	print('Part 2:', garbage)

main(sys.stdin.readline().rstrip())

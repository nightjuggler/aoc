import sys

def decompress(s, recurse):
	slen = len(s)
	dlen = 0

	def read_int(i, c):
		if i == slen or s[i] not in '123456789':
			raise SystemExit(f'Expected a digit (1-9) at position {i}!')
		j = i + 1
		while j < slen and s[j] in '0123456789':
			j += 1
		if j == slen or s[j] != c:
			raise SystemExit(f"Expected a digit or '{c}' at position {j}!")
		return j + 1, int(s[i:j])

	i = 0
	while i < slen:
		if s[i] == '(':
			i, seqlen = read_int(i + 1, 'x')
			i, repeat = read_int(i, ')')
			if i + seqlen > slen:
				raise SystemExit(f'Cannot repeat {seqlen} characters from position {i}!')

			dlen += (decompress(s[i:i+seqlen], True) if recurse else seqlen) * repeat
			i += seqlen
		elif s[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
			dlen += 1
			i += 1
		else:
			raise SystemExit(f'Expected an uppercase letter or open paren at position {i}!')
	return dlen

def main():
	line = sys.stdin.readline().rstrip()
	print('Part 1:', decompress(line, False))
	print('Part 2:', decompress(line, True))

main()

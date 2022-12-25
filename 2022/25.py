def to_snafu(n):
	assert isinstance(n, int)
	carry = 0
	digits = []
	end = (0, 0) if n >= 0 else (-1, 5)
	while True:
		n, digit = divmod(n, 5)
		digit += carry
		if (n, digit) == end: break
		carry = digit > 2
		digits.append('012=-0'[digit])
	return ''.join(digits[::-1]) or '0'

def from_snafu(n):
	n = n.strip()
	assert n and not n.strip('=-012')
	return sum(('=-012'.index(d) - 2) * 5**x for x, d in enumerate(n[::-1]))

import sys
print(to_snafu(sum(map(from_snafu, sys.stdin))))

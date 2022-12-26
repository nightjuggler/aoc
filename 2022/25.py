def to_snafu(n):
	assert isinstance(n, int)
	digits = []
	while n:
		n, digit = divmod(n, 5)
		if digit > 2: n += 1
		digits.append('012=-'[digit])
	return ''.join(digits[::-1]) or '0'

def from_snafu(n):
	n = n.strip()
	assert n and not n.strip('=-012')
	return sum(('=-012'.index(d) - 2) * 5**x for x, d in enumerate(n[::-1]))

import sys
print(to_snafu(sum(map(from_snafu, sys.stdin))))

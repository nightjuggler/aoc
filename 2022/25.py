def to_snafu(n):
	assert isinstance(n, int) and n >= 0
	carry = 0
	digits = []
	while n:
		n, digit = divmod(n, 5)
		digit += carry
		carry = digit > 2
		digits.append('012=-0'[digit])
	if carry or not digits:
		digits.append('01'[carry])
	return ''.join(digits[::-1])

def from_snafu(n):
	n = n.strip()
	assert n and not n.strip('=-012')
	return sum(('=-012'.index(d) - 2) * 5**x for x, d in enumerate(n[::-1]))

import sys
print(to_snafu(sum(map(from_snafu, sys.stdin))))

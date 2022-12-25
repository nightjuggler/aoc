import sys

def to_snafu(n):
	carry = 0
	digits = []
	while n:
		n, r = divmod(n, 5)
		r += carry
		carry = r > 2
		digits.append('012=-0'[r])
	if carry:
		digits.append('1')
	return ''.join(digits[::-1])

def main():
	snafu = {digit: value for value, digit in enumerate('=-012', start=-2)}

	def from_snafu(n):
		n = n.strip()
		assert n and not n.strip('=-012')
		return sum(snafu[d] * 5**x for x, d in enumerate(n[::-1]))

	print(to_snafu(sum(map(from_snafu, sys.stdin))))
main()

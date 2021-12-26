# This is the code generated from the puzzle input by 24.py with three lines
# added to avoid recursing deeper if z exceeds a threshold based on the
# recursion depth, i.e. based on which sections remain to be executed, since
# z cannot reach 0 once it reaches or exceeds that threshold. The thresholds
# are powers of 26 and specific to the puzzle input (which has been converted
# to Python and split up into the functions section1 through section14).
# For example, at depth 12, with sections 13 and 14 remaining, z cannot reach 0
# if it is greater than or equal to 26*26 since the only remaining operations
# that decrease z are the two divisions by 26, one in each remaining section.
# This program finds the answers to both parts 1 and 2 in about 4 seconds.

def section0(w, z):
	return z

def section1(w, z):
	x = z % 26 + 11
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 5) * x
	z += y
	return z

def section2(w, z):
	x = z % 26 + 13
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 5) * x
	z += y
	return z

def section3(w, z):
	x = z % 26 + 12
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 1) * x
	z += y
	return z

def section4(w, z):
	x = z % 26 + 15
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 15) * x
	z += y
	return z

def section5(w, z):
	x = z % 26 + 10
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 2) * x
	z += y
	return z

def section6(w, z):
	x = z % 26
	z //= 26
	x += -1
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 2) * x
	z += y
	return z

def section7(w, z):
	x = z % 26 + 14
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 5) * x
	z += y
	return z

def section8(w, z):
	x = z % 26
	z //= 26
	x += -8
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 8) * x
	z += y
	return z

def section9(w, z):
	x = z % 26
	z //= 26
	x += -7
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 14) * x
	z += y
	return z

def section10(w, z):
	x = z % 26
	z //= 26
	x += -8
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 12) * x
	z += y
	return z

def section11(w, z):
	x = z % 26 + 11
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 7) * x
	z += y
	return z

def section12(w, z):
	x = z % 26
	z //= 26
	x += -2
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 14) * x
	z += y
	return z

def section13(w, z):
	x = z % 26
	z //= 26
	x += -2
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 13) * x
	z += y
	return z

def section14(w, z):
	x = z % 26
	z //= 26
	x += -13
	x = int(x != w)
	y = 25 * x + 1
	z *= y
	y = (w + 6) * x
	z += y
	return z

sections = [
	section0,
	section1,
	section2,
	section3,
	section4,
	section5,
	section6,
	section7,
	section8,
	section9,
	section10,
	section11,
	section12,
	section13,
	section14,
]

cutoff = [0, 0, 0, 0, 0, 0, 0, 0, 26**5, 26**4, 26**3, 26**3, 26**2, 26]

def main():
	seen = set()
	digits = range(9, 0, -1)
	answer = []

	def solve(depth, w, z):
		z = sections[depth](w, z)

		if depth == 14:
			return z == 0
		if depth > 7 and z >= cutoff[depth]:
			return False

		state = (depth, z)
		if state in seen:
			return False

		for w in digits:
			if solve(depth + 1, w, z):
				answer.append(w)
				return True

		seen.add(state)
		return False

	solve(0, 0, 0)
	answer.reverse()
	print('Part 1: ', *answer, sep='')

	answer.clear()
	digits = range(1, 10)
	solve(0, 0, 0)
	answer.reverse()
	print('Part 2: ', *answer, sep='')

main()

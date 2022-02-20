from array import array

def solve_v1(n, a):
	assert n > 0 and n % 2 == 0
	assert a.strip('01') == ''

	a = [c == '1' for c in a]

	while len(a) < n:
		b = (not c for c in reversed(a))
		a.append(False)
		a.extend(b)

	while True:
		a = [b == c for b, c in zip(a[:n:2], a[1:n:2])]
		if len(a) % 2: break

	return ''.join(['01'[c] for c in a])

def solve_v2(n, a):
	assert n > 0 and n % 2 == 0
	assert a.strip('01') == ''

	pn = len(a)
	a = array('B', [c == '1' for c in a])
	a.append(False)
	a.extend(not c for c in a[-2::-1])

	while (an := len(a)) < n:
		a.append(False)
		a.extend(a[:-1])
		a[an+1+pn] = True
		pn = an

	step = (n ^ (n - 1)) // 2 + 1
	return ''.join(['10'[sum(a[i:i+step]) % 2] for i in range(0, n, step)])

def main():
	solve = solve_v2
	print('Example:', solve(20, '10000'))
	print('Part 1:', solve(272, '10001110011110000'))
	print('Part 2:', solve(35651584, '10001110011110000'))

if __name__ == '__main__':
	main()

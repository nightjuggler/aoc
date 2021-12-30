def part2valid(password, double):
	prev = password[double]
	repeat = 2
	for c in password[double + 1:]:
		if c == prev:
			repeat += 1
		elif repeat == 2:
			return True
		else:
			prev = c
			repeat = 1
	return repeat == 2

def solve(password, max_password, part2=False):
	password_len = len(password)
	assert password_len > 1
	assert password_len == len(max_password)

	password = list(map(int, password))
	max_password = list(map(int, max_password))

	double = 0
	prev = password[0]
	for i in range(1, password_len):
		c = password[i]
		if c < prev:
			c = prev
			password[i:] = [c] * (password_len - i)
			if not double:
				double = i
			break
		if c == prev and not double:
			double = i
		prev = c

	if not double:
		i = password_len - 2
		c = password[i] + 1
		password[i:] = [c] * 2
		double = i + 1

	n = 0
	while password <= max_password:
		if not part2 or part2valid(password, double):
#			print(''.join(map(str, password)), double)
			n += 1
		i = password_len - 1
		if double == i:
			i -= 1
			c = password[i]
		while c == 9:
			assert i > 0
			i -= 1
			c = password[i]
		if double >= i:
			double = i + 1
		c += 1
		password[i:] = [c] * (password_len - i)

	return n

def main():
	min_password, max_password = '153517', '630395'
	print('Part 1:', solve(min_password, max_password))
	print('Part 2:', solve(min_password, max_password, part2=True))

if __name__ == '__main__':
	main()

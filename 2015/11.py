def update_password(password, skip):
	plen = len(password)

	while True:
		i = plen - 1
		while password[i] == 25:
			password[i] = 0
			i -= 1
			if i < 0:
				i = plen - 1
				password[i] = -1
				break

		password[i] += 1
		if password[i] in skip:
			password[i] += 1
			for j in range(i + 1, plen):
				password[j] = 0

		pair1 = pair2 = straight = None
		q = p = None

		for i in range(plen):
			c = password[i]
			if c in skip:
				password[i] = c = c + 1
				for j in range(i + 1, plen):
					password[j] = 0
			elif c == p:
				if not pair1:
					pair1 = i
				elif not pair2 and i > pair1 + 1:
					pair2 = i
			elif i > 1 and c == p + 1 and c == q + 2 and not straight:
				straight = i
			q = p
			p = c

		if pair1 and pair2 and straight:
			break

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('password', nargs='?', default='cqjxjnds')
	args = parser.parse_args()

	password = [ord(c) - 97 for c in args.password]
	if len(password) < 5:
		print('The password must be at least 5 letters long!')
		return

	for c in password:
		if c < 0 or c > 25:
			print('The password must contain only lowercase letters!')
			return

	skip = set([ord(c) - 97 for c in 'ilo'])

	update_password(password, skip)

	print(''.join([chr(97 + c) for c in password]))

if __name__ == '__main__':
	main()

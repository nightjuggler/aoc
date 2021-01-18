def update_password(password, skip):
	plen = len(password)
	pair1 = pair2 = straight = None
	first = True
	i = plen - 1

	while not (pair1 and pair2 and straight):
		while password[i] == 25:
			password[i] = 0
			i -= 1
			if i < 0:
				i = plen - 1
				password[i] = -1
		password[i] += 1

		if first:
			i = 0
			first = False
		else:
			if pair1:
				if pair1 >= i:
					pair1 = pair2 = None
				elif pair2 and pair2 >= i:
					pair2 = None
			if straight and straight >= i:
				straight = None

		p = password[i-1] if i > 0 else None

		for i in range(i, plen):
			c = password[i]
			if c in skip:
				password[i] = c = c + 1
				for j in range(i + 1, plen):
					password[j] = 0
			if c == p:
				if not pair1:
					pair1 = i
				elif not pair2 and i > pair1 + 1:
					pair2 = i
			elif i > 1 and c == p + 1 and c == password[i-2] + 2 and not straight:
				straight = i
			p = c

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

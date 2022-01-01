import hashlib
import sys

def main():
	door = sys.argv[1] if len(sys.argv) > 1 else 'ojvtpuvg'
	door = door.encode('ascii')

	password1 = []
	password2 = ['_'] * 8
	left1 = 8
	left2 = 8
	n = 0
	while left2:
		while True:
			md5 = hashlib.md5()
			md5.update(door)
			md5.update(str(n).encode('ascii'))
			n += 1
			if md5.hexdigest()[:5] == '00000':
				break
		hash = md5.hexdigest()
		if left1:
			password1.append(hash[5])
			left1 -= 1
		i = ord(hash[5]) - 48
		if 0 <= i <= 7 and password2[i] == '_':
			password2[i] = hash[6]
			left2 -= 1
		print(*password1, ', ', *password2, sep='')

	print('Part 1: ', *password1, sep='')
	print('Part 2: ', *password2, sep='')

if __name__ == '__main__':
	main()

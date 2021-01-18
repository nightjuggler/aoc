import hashlib
import sys

def main():
	data = sys.argv[1] if len(sys.argv) > 1 else 'yzbqklnj'
	data = data.encode('ascii')

	n = 0
	while True:
		n += 1
		md5 = hashlib.md5()
		md5.update(data)
		md5.update(str(n).encode('ascii'))
		if md5.hexdigest()[:6] == '000000':
			break
	print(n)

if __name__ == '__main__':
	main()

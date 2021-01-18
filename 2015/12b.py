import json
import sys

def typestr(o):
	return str(o) + ' is ' + type(o).__name__

def add_numbers(o):
	if isinstance(o, str):
		return 0
	if isinstance(o, int):
		return o
	if isinstance(o, list):
		n = 0
		for e in o:
			n += add_numbers(e)
		return n
	if isinstance(o, dict):
		n = 0
		for k, v in o.items():
			if v == 'red':
				return 0
			if not isinstance(k, str):
				print('Expected str for dict key!', typestr(k))
			n += add_numbers(v)
		return n

	print('Expected str, int, list, or dict!', typestr(o))
	return 0

def main():
	try:
		o = json.load(sys.stdin)
	except json.decoder.JSONDecodeError as e:
		print(e)
		return
	print(add_numbers(o))

if __name__ == '__main__':
	main()

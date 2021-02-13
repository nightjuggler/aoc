import sys

def main():
	data = map(int, sys.stdin.readline().split())

	def add_metadata():
		num_children = next(data)
		num_metadata = next(data)
		metadata_sum = 0
		for i in range(num_children):
			metadata_sum += add_metadata()
		for i in range(num_metadata):
			metadata_sum += next(data)
		return metadata_sum

	metadata_sum = add_metadata()
	assert len(list(data)) == 0
	print(metadata_sum)

if __name__ == '__main__':
	main()

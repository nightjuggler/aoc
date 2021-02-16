import sys

def main():
	target = 825401
	if len(sys.argv) > 1:
		try:
			target = int(sys.argv[1])
		except ValueError:
			target = 0
		if target < 2:
			print('The number of recipes must be >= 2!')
			return

	target += 10
	recipes = [3, 7]
	num_recipes = 2
	i1 = 0
	i2 = 1

	while num_recipes < target:
		elf1 = recipes[i1]
		elf2 = recipes[i2]
		new_recipe = elf1 + elf2
		if new_recipe >= 10:
			recipes.append(1)
			recipes.append(new_recipe - 10)
			num_recipes += 2
		else:
			recipes.append(new_recipe)
			num_recipes += 1
		i1 = (i1 + elf1 + 1) % num_recipes
		i2 = (i2 + elf2 + 1) % num_recipes

	print(''.join([str(r) for r in recipes[target-10:target]]))

if __name__ == '__main__':
	main()

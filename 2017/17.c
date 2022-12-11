#include <stdio.h>
#include <stdlib.h>

typedef unsigned int uint;

uint part1(uint steps, const uint num_values)
{
	uint *after, after_last = 0;
	steps -= 1;
	if ((after = (uint *)calloc(num_values + 1, sizeof(uint))) == NULL)
		return -1;
	for (uint value = 1; value <= num_values; value++)
	{
		uint pos = after_last;
		for (uint i = steps; i > 0; --i) pos = after[pos];
		after[value] = after_last = after[pos];
		after[pos] = value;
	}
	free(after);
	return after_last;
}
uint part2(const uint steps, const uint num_values)
{
	uint pos = 0, after0 = 0;
	for (uint value = 1; value <= num_values; value++, pos++)
		if ((pos = (pos + steps) % value) == 0) after0 = value;
	return after0;
}
int main(int argc, char **argv)
{
	uint steps = 328;
	if (argc >= 2) {
		char *endptr;
		if (argc > 2) {
			fprintf(stderr, "Please specify at most one argument!\n");
			return 1;
		}
		steps = strtoul(argv[1], &endptr, 10);
		if (!steps || *endptr || steps > (1<<16)) {
			fprintf(stderr, "Please specify a valid number of steps!\n");
			return 1;
		}
	}
	printf("Part 1: %u\n", part1(steps, 2017));
	printf("Part 2: %u\n", part2(steps, 50000000));
	return 0;
}

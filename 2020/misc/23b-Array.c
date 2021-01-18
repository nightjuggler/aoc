#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv)
{
	int h, x, y, z, d, *next;
	unsigned int num_cups = 1000000;
	unsigned int num_moves = 10000000;
	char *input_string = "463528179";
	clock_t t1, t2;
	int i, j, p;

	t1 = clock();

	if ((next = (int *)malloc((num_cups + 1) * sizeof(int))) == NULL) {
		printf("malloc failed!\n");
		return 1;
	}
	h = p = input_string[0] - 48;
	for (i = 1; i < 9; ++i)
	{
		next[p] = j = input_string[i] - 48;
		p = j;
	}
	while (++i <= num_cups)
	{
		next[p] = i;
		p = i;
	}
	next[p] = h;

	t2 = clock();
	printf("Init: %fs\n", (double)(t2 - t1) / CLOCKS_PER_SEC);
	t1 = clock();

	for (i = num_moves; i != 0; --i)
	{
		x = next[h];
		y = next[x];
		z = next[y];

		d = h == 1 ? num_cups : h - 1;

		while (d == x || d == y || d == z)
			d = d == 1 ? num_cups : d - 1;

		next[h] = next[z];
		next[z] = next[d];
		next[d] = x;
		h = next[h];
	}

	x = next[1];
	y = next[x];
	printf("%u * %u = %lu\n", x, y, (unsigned long)x * (unsigned long)y);

	t2 = clock();
	printf("Game: %fs\n", (double)(t2 - t1) / CLOCKS_PER_SEC);

	free(next);
	return 0;
}

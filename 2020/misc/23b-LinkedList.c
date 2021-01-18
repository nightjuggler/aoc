#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct Elem *Eptr;
struct Elem {
	int value;
	Eptr next;
	Eptr dest;
};

int main(int argc, char **argv)
{
	Eptr h, x, y, z, d;
	Eptr head, curr, next, prev;
	Eptr m[10];
	unsigned int num_cups = 1000000;
	unsigned int num_moves = 10000000;
	char *input_string = "463528179";
	clock_t t1, t2;
	int i, j;

	t1 = clock();

	if ((head = (Eptr)malloc(num_cups * sizeof(struct Elem))) == NULL) {
		printf("malloc failed!\n");
		return 1;
	}

	for (i = 0, curr = head; i < 9; ++i, ++curr)
	{
		curr->value = j = input_string[i] - 48;
		m[j] = curr;
	}

	curr = head + num_cups - 1;
	next = head;
	prev = m[1];
	i = num_cups;

	while (i > 9)
	{
		curr->value = i--;
		curr->next = next;
		prev = prev->dest = curr;
		next = curr--;
	}
	while (i > 0)
	{
		curr->next = next;
		prev = prev->dest = m[i--];
		next = curr--;
	}

	t2 = clock();
	printf("Init: %fs\n", (double)(t2 - t1) / CLOCKS_PER_SEC);
	t1 = clock();

	h = head;
	for (i = num_moves; i != 0; --i)
	{
		x = h->next;
		y = x->next;
		z = y->next;

		d = h->dest;
		while (d == x || d == y || d == z)
			d = d->dest;

		h->next = z->next;
		z->next = d->next;
		d->next = x;
		h = h->next;
	}
	while (h->value != 1)
		h = h->next;

	x = h->next;
	y = x->next;
	i = x->value;
	j = y->value;
	printf("%u * %u = %lu\n", i, j, (unsigned long)i * (unsigned long)j);

	t2 = clock();
	printf("Game: %fs\n", (double)(t2 - t1) / CLOCKS_PER_SEC);

	free(head);
	return 0;
}

#include <stdio.h>

typedef unsigned int uint;
typedef unsigned long long ull;

#define M_BITS 31
const ull M = (1ull<<M_BITS)-1; // 2147483647

// Since M = 2^K - 1, x % M is equal to (xhi + xlo) % M where
// xlo = x & M, i.e. the K low bits of M, and
// xhi = x >> K, i.e. the high bits of M (bits K+1 and higher)
// This is because x = (2^K)*xhi + xlo = (2^K - 1)*xhi + xhi + xlo = M*xhi + xhi + xlo
// So x % M = (xhi + xlo) % M

// Since the factor c by which x is multiplied is at most 16 bits (48271),
// x * c will be at most 31 + 16 = 47 bits (2147483646 * 48271)
// Thus xhi will be at most 16 bits, and xhi + xlo will be at most 32 bits and less than 2*M
// So to compute (xhi + xlo) % M (and thus x % M), we can just subtract M if xhi + xlo >= M

// The program runs approx. 180ms faster (~330ms vs. ~510ms) using this method
// of computing x % M without the remainder operator:

// >>> TIMEFMT="%*E seconds"
// >>> clang -O2 15.c
// >>> time ./a.out < data/15.input
// Part 1: 650
// Part 2: 336
// 0.510 seconds
// >>> clang -O2 -DNOMOD 15.c
// >>> time ./a.out < data/15.input
// Part 1: 650
// Part 2: 336
// 0.330 seconds

#ifdef NOMOD
#define GENERATE1(x, c) x *= c; x = (x & M) + (x >> M_BITS); if (x >= M) x -= M
#define GENERATE2(x, c, d) do { GENERATE1(x, c); } while (x & (d-1))
#else
#define GENERATE1(x, c) x = x * c % M
#define GENERATE2(x, c, d) while ((GENERATE1(x, c)) % d)
#endif

int readline(char expected_label, ull *start)
{
	char label;
	if (scanf(" Generator %c starts with %llu", &label, start) != 2
		|| label != expected_label)
	{
		fprintf(stderr, "Could not read starting value for generator %c!\n", expected_label);
		return 1;
	}
	return 0;
}
uint part1(ull a, ull b)
{
	const uint m = (1<<16)-1;
	uint n = 0;
	for (uint i = 0; i < 40000000; i++)
	{
		GENERATE1(a, 16807);
		GENERATE1(b, 48271);
		if ((a & m) == (b & m)) ++n;
	}
	return n;
}
uint part2(ull a, ull b)
{
	const uint m = (1<<16)-1;
	uint n = 0;
	for (uint i = 0; i < 5000000; i++)
	{
		GENERATE2(a, 16807, 4);
		GENERATE2(b, 48271, 8);
		if ((a & m) == (b & m)) ++n;
	}
	return n;
}
int main(int argc, char **argv)
{
	ull a, b;
	if (readline('A', &a) != 0 || readline('B', &b) != 0)
		return 1;

	printf("Part 1: %u\n", part1(a, b));
	printf("Part 2: %u\n", part2(a, b));
	return 0;
}

#include <stdio.h>
#include <string.h>
/*
	Part 1:
	> gcc -DREPEAT=1 -DSKIPLEN=0 16.c
	> echo 80871224585914546619083218645595 | ./a.out
	24176176
	> ./a.out < data/16.input

	Part 2:
	> gcc 16.c
	> echo 03036732577212944063491565474664 | ./a.out
	84462026
	> ./a.out < data/16.input
*/
#ifndef MAXLEN
#define MAXLEN 650
#endif
#ifndef MSGLEN
#define MSGLEN 8
#endif
#ifndef PHASES
#define PHASES 100
#endif
#ifndef REPEAT
#define REPEAT 10000
#endif
#ifndef SKIPLEN
#define SKIPLEN 7
#endif

#define BUFSIZE MAXLEN+2 < MAXLEN*REPEAT ? MAXLEN*REPEAT : MAXLEN+2

typedef unsigned char uchar;
typedef unsigned int uint;

void fft(uchar *in, uchar *out, const uint len, const uint skip)
{
	uint pos = len;
	uchar last = 0;
	uint k = len >> 1;
	if (skip > k) k = skip;
	while (pos > k)
	{
		--pos;
		last = out[pos] = (in[pos] + last) % 10;
	}
	in += skip;
	out += skip;
	pos -= skip;
	while (pos)
	{
		long sum = 0;
		uint i, j;
		for (i = pos - 1; i < len; i += pos)
		{
			if ((j = i + pos) > len) j = len;
			while (i < j)
				sum += in[i++];

			if ((i += pos) >= len) break;

			if ((j = i + pos) > len) j = len;
			while (i < j)
				sum -= in[i++];
		}
		if (sum < 0) sum = -sum;
		out[--pos] = sum % 10;
	}
}

int main(int argc, char **argv)
{
	static uchar buf1[BUFSIZE];
	static uchar buf2[BUFSIZE];
	uchar *tmp;
	uchar *in = buf1;
	uchar *out = buf2;
	uint skip = 0;
	uint len = 0;

	if (!fgets((char *)in, MAXLEN+2, stdin)) {
		fprintf(stderr, "Failed to read from standard input!\n");
		return 1;
	}
	len = strlen((char *)in);
	if (len > 0 && in[len-1] == '\n')
		in[--len] = 0;
	else if (len > MAXLEN) {
		fprintf(stderr, "Input too long!\n");
		return 1;
	}
	if (len < SKIPLEN) {
		fprintf(stderr, "Input too short!\n");
		return 1;
	}
	for (uint i = 0; i < len; ++i)
	{
		uchar ch = in[i];
		if (ch < '0' || ch > '9') {
			fprintf(stderr, "Input not valid!\n");
			return 1;
		}
		in[i] = ch - '0';
	}
	for (uint i = 0; i < SKIPLEN; ++i)
		skip = skip * 10 + in[i];
	if (skip + MSGLEN > len*REPEAT)
	{
		fprintf(stderr, "Input too short for message offset!\n");
		return 1;
	}
	tmp = in;
	for (uint i = 1; i < REPEAT; ++i)
		memcpy(tmp += len, in, len);
	len *= REPEAT;
	for (uint i = 0; i < PHASES; ++i)
	{
		fft(in, out, len, skip);
		tmp = in;
		in = out;
		out = tmp;
	}
	in += skip;
	for (uint i = 0; i < MSGLEN; ++i)
		printf("%c", '0' + in[i]);
	printf("\n");
	return 0;
}

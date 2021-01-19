#include <stdio.h>
#include <string.h>

int update_password(char *password)
{
	const int plen = strlen(password);
	int pair1 = 0;
	int pair2 = 0;
	int straight = 0;
	int first = 1;
	int i = plen;
	int j;
	char c, p;

	if (plen < 5) {
		printf("The password must be at least 5 letters long!\n");
		return 1;
	}
	for (j = plen - 1; j >= 0; --j)
		if ((c = password[j]) < 'a' || c > 'z') {
			printf("The password must contain only lowercase letters!\n");
			return 1;
		}

	while (!(pair1 && pair2 && straight))
	{
		while (password[--i] == 'z')
		{
			password[i] = 'a';
			if (i == 0) {
				password[i = plen - 1] = 'a' - 1;
				break;
			}
		}
		password[i] += 1;

		if (first) {
			i = 0;
			first = 0;
		} else {
			if (pair1 >= i) {
				pair1 = 0;
				pair2 = 0;
			} else if (pair2 >= i)
				pair2 = 0;
			if (straight >= i)
				straight = 0;
		}

		p = i > 0 ? password[i-1] : 0;
		for (; i < plen; ++i)
		{
			c = password[i];
			if (c == 'i' || c == 'l' || c == 'o') {
				password[i] = c += 1;
				for (j = i + 1; j < plen; ++j)
					password[j] = 'a';
			}
			if (c == p) {
				if (!pair1)
					pair1 = i;
				else if (!pair2 && i > pair1 + 1)
					pair2 = i;
			} else if (i > 1 && c == p + 1 && c == password[i-2] + 2 && !straight)
				straight = i;
			p = c;
		}
	}

	printf("%s\n", password);
	return 0;
}

int main(int argc, char **argv)
{
	char password[] = "cqjxjnds";
	return update_password(argc > 1 ? argv[1] : password);
}

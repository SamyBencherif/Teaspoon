
/** Normally, this file will contain dynamically generated links to installed extensions */

void b_print(Array v)
{
	int i=0;
	while (i < v.len)
	{
		printf("%c", (char)v.get[i]);
		i++;
	}
}
